const iClick = require('iclick-auto')

let iclient = null

async function connect(options = {}) {

    if( iclient ){
        await iclient.destroy()
    }

    iclient = iClick(options)
    await iclient.connect()
}

async function invoke(type, params = {}, timeout = 18) {

    if( !iclient ){
        throw new Error('iclick 未连接，请先调用 connect()')
    }

    return iclient.invoke(type, params, timeout)
}

module.exports = {
    connect,
    invoke,
    get client() {
        return iclient
    },
}
