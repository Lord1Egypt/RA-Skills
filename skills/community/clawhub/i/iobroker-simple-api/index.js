/**
 * ioBroker Simple-API Skill Loader
 * This wrapper properly loads the skill module using VM to avoid module shadowing issues
 */

const fs = require('fs');
const vm = require('vm');
const path = require('path');

// Get __dirname equivalent for this file
const skillDir = __dirname;

// Read the skill implementation
const skillCode = fs.readFileSync(path.join(skillDir, 'skill.js'), 'utf8');

// Create a proper module context - preserve original process.env
const moduleContext = {
    module: { exports: {} },
    exports: {},
    require: require,
    console: console,
    setTimeout: setTimeout,
    clearTimeout: clearTimeout,
    setInterval: setInterval,
    clearInterval: clearInterval,
    https: require('https'),
    http: require('http'),
    URL: require('url').URL,
    URLSearchParams: require('url').URLSearchParams,
    Buffer: Buffer,
    process: {
        env: {
            // Use existing OPENCLAW_HOME or HOME from parent process
            OPENCLAW_HOME: process.env.OPENCLAW_HOME,
            HOME: process.env.HOME
        }
    }
};

// Link module.exports to exports
moduleContext.module.exports = moduleContext.exports;

// Run the skill code in the VM context
vm.runInContext(skillCode, vm.createContext(moduleContext));

// Export the loaded skill
module.exports = moduleContext.module.exports;
module.exports.default = moduleContext.module.exports;