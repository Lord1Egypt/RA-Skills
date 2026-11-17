"use strict";
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
exports.initCommand = void 0;
const commander_1 = require("commander");
const inquirer_1 = __importDefault(require("inquirer"));
const fs_1 = __importDefault(require("fs"));
const path_1 = __importDefault(require("path"));
exports.initCommand = new commander_1.Command('init').description('Create an explicit local Guard configuration').action(async () => {
    const { dir, secureDir } = require('../../../transport');
    const { mode } = await inquirer_1.default.prompt([{ type: 'list', name: 'mode', message: 'Runtime policy mode', choices: [{ name: 'Passive: no execution protection', value: 'passive' }, { name: 'Full: block unless authenticated policy grants execution', value: 'full' }], default: 'passive' }]);
    secureDir(dir());
    fs_1.default.writeFileSync(path_1.default.join(dir(), 'config.json'), JSON.stringify({ version: '3.0.0', mode }, null, 2), { mode: 0o600, flag: 'wx' });
    console.log('Configuration created. Provision trusted skill keys, allowed-skills.json and policy.json before starting the daemon.');
});
//# sourceMappingURL=init.js.map