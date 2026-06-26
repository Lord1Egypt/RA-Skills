#!/usr/bin/env node
const path = require('path')
const iclick = require('./util/iclick')

function handleError(_error) {
    console.error(JSON.stringify({ status: false, message: _error.message }))
    process.exit(1)
}

;(async () => {
    const _method = process.argv[2]
    const _paramsRaw = process.argv[3]

    if (!_method) {
        handleError(new Error('请传入方法名，例如: node server.js getDevices'))
    }
    if (!/^[a-zA-Z0-9_]+$/.test(_method)) {
        handleError(new Error('方法名只能包含字母、数字、下划线'))
    }

    try {

        await iclick.connect()

        const _params = _paramsRaw ? JSON.parse(_paramsRaw) : {}
   
        let _result = null
        try {
            const _cmd = require(path.join(__dirname, 'command', _method + '.js'))
            _result = await _cmd.run(_params)
        } catch (_error) {
            _result = await iclick.invoke(_method, _params)
        }
        
        console.log(JSON.stringify(_result, null, 2))

        process.exit(0)
    } catch (_error) {
        if (_error instanceof SyntaxError) {
            handleError(new Error('参数必须是合法 JSON，例如: node server.js getScreenShot \'{"deviceId":"xxx"}\''))
        } else {
            handleError(_error)
        }
    }
})()
