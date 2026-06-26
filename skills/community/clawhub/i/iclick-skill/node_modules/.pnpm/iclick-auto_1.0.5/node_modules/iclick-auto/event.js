function createEventEmitter() {
    const eventListeners = {}

    function on(eventName, callback) {
        if( typeof callback !== 'function' ){
            throw new Error('callback must be a function')
        }
        if( !eventListeners[eventName] ){
            eventListeners[eventName] = []
        }
        eventListeners[eventName].push(callback)
    }

    function off(eventName, callback) {
        if( !eventListeners[eventName] ){
            return
        }
        if( callback ){
            const index = eventListeners[eventName].indexOf(callback)
            if( index > -1 ){
                eventListeners[eventName].splice(index, 1)
            }
        }else{
            delete eventListeners[eventName]
        }
    }

    function emit(eventName, data) {
        const listeners = eventListeners[eventName]
        if( listeners && listeners.length > 0 ){
            listeners.forEach(callback => {
                try {
                    callback(data)
                } catch (error) {
                    console.error('事件监听器执行错误:', error)
                }
            })
        }
    }

    function clearAll() {
        Object.keys(eventListeners).forEach(eventName => {
            delete eventListeners[eventName]
        })
    }

    return {
        on,
        off,
        emit,
        clearAll,
    }
}

module.exports = createEventEmitter

