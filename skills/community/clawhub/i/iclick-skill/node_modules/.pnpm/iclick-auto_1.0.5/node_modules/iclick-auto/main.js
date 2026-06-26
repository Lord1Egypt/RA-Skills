const WebSocket = require('ws')
const { websocket_host, websocket_port, reconnect_delay, max_reconnect_attempts } = require('./utils')
const createEventEmitter = require('./event')

function createClient(options = {}) {
    
    const wsevents = {}
    const eventEmitter = createEventEmitter()
    let wsclient = null
    let reconnectTimer = null
    let closed = false
    let reconnectAttempts = 0
    const host = options.host || websocket_host
    const port = options.port || websocket_port
    const autoReconnect = options.autoReconnect !== false  // 默认启用自动重连
    const reconnectDelay = options.reconnectDelay || reconnect_delay  // 默认重连延迟（秒）
    const maxAttempts = options.maxReconnectAttempts || max_reconnect_attempts  // 最大重连重试次数

    function reconnect() {
        if( closed || !autoReconnect ){
            return
        }
        if( reconnectTimer || (wsclient && wsclient.readyState === WebSocket.CONNECTING) ){
            return
        }
        if( reconnectAttempts >= maxAttempts ){
            console.error(`[iClick] Max reconnect attempts (${maxAttempts}) reached. Stopping reconnection.`)
            return
        }
        reconnectAttempts++
        reconnectTimer = setTimeout(() => {
            connectServer().finally(() => reconnectTimer = null)
        }, reconnectDelay * 1000)
    }

    function connectServer() {
        return new Promise((_resolve, _reject) => {
            
            if( wsclient ){
                return _resolve()
            }

            wsclient = new WebSocket(`ws://${host}:${port}`)

            wsclient.on('open', () => {
                reconnectAttempts = 0  // 连接成功后重置重连计数
                _resolve()
            })

            wsclient.on('message', (_data) => {

                let _payload = null,
                    _bindata = null

                try {
                    const _firstByte = _data[0]
                    const _isJson = _firstByte === 0x7B || _firstByte === 0x5B  // { 或 [
                    
                    if (_isJson) {
                        _payload = JSON.parse(_data.toString('utf-8'))
                    } else {

                        // binary: [metaDataLength][metaData][binary]
                        const _metaLength = _data.slice(0, 6).toString('utf-8').trim()
                        const _metaLengthInt = parseInt(_metaLength, 10)

                        _bindata = _data.slice(6 + _metaLengthInt)

                        const _metaJson = _data.slice(6, 6 + _metaLengthInt).toString('utf-8')

                        _payload = JSON.parse(_metaJson)
                        _payload.data = _bindata
                        _bindata = null
                    }
                } catch (_error) {
                    console.error('[iClick] receive message error:', _error.message)
                    return _reject(_error)
                }
                
                const _eventId = _payload.evtid
                const _event = wsevents[ _eventId ]
      
                if( _event ){

                    if( _payload.type === 'error' ){
                        _event.reject(new Error(_payload.error))
                    }else{
                        _event.resolve( _payload.data )
                    }

                    delete wsevents[ _eventId ]

                }else if( _payload.event ){

                    eventEmitter.emit(_payload.event, _payload.data)
                }
            })
            
            wsclient.on('close', (_code) => {
                wsclient = null
                if( !closed ){
                    reconnect()
                }
            })
            
            wsclient.on('error', (_err) => {
                _reject(_err)
            })
        })
    }

    function apiInvoke(type, _params = {}, _timeout = 18) {

        return new Promise((_resolve, _reject) => {

            if( !wsclient || wsclient.readyState !== WebSocket.OPEN ){

                _reject( new Error('websocket not connected') )

            }else{

                const _eventId = Math.random().toString(36).substring(2, 12)
                const _payload = {
                    ..._params,
                    type,
                    evtid: _eventId,
                    timeout: _timeout
                }

                wsevents[_payload.evtid] = { resolve: _resolve, reject: _reject }

                wsclient.send(JSON.stringify(_payload))

                if( _timeout > 0 ){
                    setTimeout(() => {

                        if( wsevents[_payload.evtid] ){
                            _reject(new Error(`API: ${_payload.evtid} => ${_payload.type} Invoke Timeout !`))
                            delete wsevents[_payload.evtid]
                        }

                    }, _timeout * 1000)
                }
            }
        })
    }

    function destroy() {

        closed = true

        if( reconnectTimer ){
            clearTimeout(reconnectTimer)
            reconnectTimer = null
        }

        if( wsclient ){
            wsclient.removeAllListeners()
            if( wsclient.readyState === WebSocket.OPEN || wsclient.readyState === WebSocket.CONNECTING ){
                wsclient.close()
            }
            wsclient = null
        }

        eventEmitter.clearAll()

        Object.keys(wsevents).forEach(eventId => {
            const event = wsevents[eventId]
            if( event ){
                event.reject(new Error('iclick client is destroyed'))
            }
        })
    }

    return {
        connect: connectServer,
        invoke: apiInvoke,
        on: eventEmitter.on,
        off: eventEmitter.off,
        destroy,
    }
}

module.exports = createClient