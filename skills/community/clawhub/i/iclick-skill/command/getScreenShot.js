const fs = require('fs').promises
const path = require('path')
const os = require('os')
const { invoke } = require('../util/iclick')

module.exports = {
    name: 'getScreenShot',
    run: async (_params) => {

        const _data = await invoke('getScreenShot', _params)
        const _file = path.join(os.tmpdir(), `${Math.random().toString(36).substring(2, 15)}.jpg`)

        await fs.writeFile(_file, _data)

        return { status: true, message: `已保存`, file: _file }
    },
}
