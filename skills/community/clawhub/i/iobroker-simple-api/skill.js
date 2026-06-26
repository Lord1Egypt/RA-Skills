/**
 * ioBroker Simple-API Skill
 * Full access to ioBroker via simple-api REST adapter
 * 
 * Read Operations:
 *   getPlainValue:<stateID>?json&noStringify - Get state value (with optional JSON parsing)
 *   get:<stateID> - Get state + object data
 *   getBulk:<stateID1,stateID2> - Get multiple states
 *   objects:<pattern>?type=<type> - List objects (optional type filter)
 *   states:<pattern> - List states matching pattern
 *   search:<pattern> - Search data points
 *   query:<stateID>?dateFrom=<date>&dateTo=<date>&noHistory&aggregate=<type>&count=<n>
 *   enums - List all enums
 *   folders - List all folders
 *   subscribe:<stateID> - Subscribe to state changes (long-poll)
 * 
 * Write Operations:
 *   set:<stateID>?value=<value>&type=<type>&ack=<true|false>&wait=<ms>
 *   toggle:<stateID> - Toggle boolean/number values
 *   setBulk:<stateID1>=<value1>&<stateID2>=<value2>
 *   create:<stateID>?common=<json>&native=<json> - Create a new state
 * 
 * Script Execution:
 *   exec:<javascript> - Execute JavaScript in ioBroker (javascript.0)
 *   eval:<expression> - Shortcut for exec
 * 
 * Examples:
 *   getPlainValue:javascript.0.data?json - Parse JSON string to object
 *   set:javascript.0.test?value=1&ack=true - Set value with acknowledgment
 *   query:system.host.*?dateFrom=-1h&aggregate=minmax - Query last hour
 *   create:javascript.0.myNewState?common={"name":"Test","type":"number"} - Create state
 *   subscribe:javascript.0.sensor.temperature - Long-poll for changes
 *   exec:$('stateID').val(true) - Execute JavaScript
 *   eval:2+2 - Quick calculation
 */

const https = require('https');
const http = require('http');
const { URL } = require('url');
const fs = require('fs');
const path = require('path');

// ============================================================================
// Configuration - Read-only from fixed paths
// ============================================================================

function getOpenClawConfig() {
    // Fixed paths only - no environment probing
    const fixedPaths = [
        process.env.OPENCLAW_HOME ? process.env.OPENCLAW_HOME + '/openclaw.json' : null,
        process.env.HOME + '/.openclaw/openclaw.json'
    ];
    
    for (const configPath of fixedPaths) {
        try {
            if (fs.existsSync(configPath)) {
                const configData = fs.readFileSync(configPath, 'utf8');
                const config = JSON.parse(configData);
                // Look in skills.entries
                const iobConfig = config.skills?.entries?.['iobroker-simple-api']?.config;
                if (iobConfig) {
                    return iobConfig;
                }
            }
        } catch (e) {
            // Continue to next path
        }
    }
    return null;
}

// Read config (read-only, no writes)
const IOBROKER_CONFIG = getOpenClawConfig();

// Configuration
const CONFIG = {
    baseUrl: IOBROKER_CONFIG ? `${IOBROKER_CONFIG.url}:${IOBROKER_CONFIG.port}` : 'http://CHANGE_ME_IP:8087',
    timeout: 10000,
    username: IOBROKER_CONFIG?.username || '',
    password: IOBROKER_CONFIG?.password || ''
};

// Track if credentials are required (determined after first API call)
let CREDENTIALS_REQUIRED = false;

// Test/Mock mode for offline testing
let MOCK_MODE = false;
const MOCK_STATES = new Map(); // Mock state storage

// ============================================================================
// Helper Functions
// ============================================================================

function getHomeDir() {
    return process.env.HOME || process.env.USERPROFILE || '/home/openclaw';
}

function buildUrl(endpoint, queryParams = {}) {
    const url = new URL(`${CONFIG.baseUrl}/${endpoint}`);
    for (const [key, value] of Object.entries(queryParams)) {
        if (value !== undefined && value !== null) {
            url.searchParams.append(key, value);
        }
    }
    return url;
}

function makeRequest(urlString, options = {}) {
    return new Promise((resolve, reject) => {
        const parsedUrl = new URL(urlString);
        const isHttps = parsedUrl.protocol === 'https:';
        const lib = isHttps ? https : http;
        
        const requestOptions = {
            hostname: parsedUrl.hostname,
            port: parsedUrl.port || (isHttps ? 443 : 80),
            path: parsedUrl.pathname + parsedUrl.search,
            method: options.method || 'GET',
            headers: {
                'Accept': 'application/json',
                'User-Agent': 'OpenClaw-ioBroker-Skill/1.0'
            },
            timeout: CONFIG.timeout
        };
        
        // Add auth header if credentials provided
        if (CONFIG.username && CONFIG.password) {
            const auth = Buffer.from(CONFIG.username + ':' + CONFIG.password).toString('base64');
            requestOptions.headers['Authorization'] = 'Basic ' + auth;
        }
        
        if (options.body) {
            requestOptions.headers['Content-Type'] = 'application/json';
            requestOptions.body = options.body;
        }
        
        const req = lib.request(requestOptions, (res) => {
            let data = '';
            res.on('data', chunk => data += chunk);
            res.on('end', () => {
                if (res.statusCode >= 200 && res.statusCode < 300) {
                    try {
                        resolve(JSON.parse(data));
                    } catch {
                        resolve(data);
                    }
                } else if (res.statusCode === 401 || res.statusCode === 403) {
                    CREDENTIALS_REQUIRED = true;
                    reject(new Error(`Authentication required (HTTP ${res.statusCode}). Please configure username and password in OpenClaw config.`));
                } else {
                    reject(new Error(`HTTP ${res.statusCode}: ${data}`));
                }
            });
        });
        
        req.on('error', reject);
        req.on('timeout', () => {
            req.destroy();
            reject(new Error('Request timeout'));
        });
        
        if (options.body) {
            req.write(options.body);
        }
        req.end();
    });
}

// ============================================================================
// API Operations
// ============================================================================

async function getPlainValue(stateId, options = {}) {
    const url = buildUrl(`getPlainValue/${stateId}`, options);
    const result = await makeRequest(url.toString());
    return options.json ? JSON.parse(result) : result;
}

async function getState(stateId) {
    const url = buildUrl(`get/${stateId}`);
    return makeRequest(url.toString());
}

async function getBulk(stateIds) {
    const ids = Array.isArray(stateIds) ? stateIds.join(',') : stateIds;
    const url = buildUrl(`getBulk/${ids}`);
    return makeRequest(url.toString());
}

async function getObjects(pattern, options = {}) {
    const url = buildUrl(`objects/${pattern}`, options);
    return makeRequest(url.toString());
}

async function getStates(pattern) {
    const url = buildUrl(`states/${pattern}`);
    return makeRequest(url.toString());
}

async function searchDataPoints(pattern) {
    const url = buildUrl(`search/${pattern}`);
    return makeRequest(url.toString());
}

async function queryHistory(stateId, options = {}) {
    const url = buildUrl(`query/${stateId}`, options);
    return makeRequest(url.toString());
}

async function getEnums() {
    const url = buildUrl('enums');
    return makeRequest(url.toString());
}

async function getFolders() {
    const url = buildUrl('folders');
    return makeRequest(url.toString());
}

async function subscribeState(stateId) {
    const url = buildUrl(`subscribe/${stateId}`);
    return makeRequest(url.toString());
}

async function setState(stateId, value, options = {}) {
    const params = { value, ...options };
    const url = buildUrl(`set/${stateId}`, params);
    return makeRequest(url.toString());
}

async function toggleState(stateId) {
    const url = buildUrl(`toggle/${stateId}`);
    return makeRequest(url.toString());
}

async function setBulk(states) {
    const url = buildUrl('setBulk', states);
    return makeRequest(url.toString());
}

async function createState(stateId, common = {}, native = {}) {
    const body = JSON.stringify({ common, native });
    const url = buildUrl(`create/${stateId}`);
    return makeRequest(url.toString(), { method: 'POST', body });
}

async function executeScript(code) {
    const url = buildUrl('exec', { script: code });
    return makeRequest(url.toString());
}

async function evalExpression(expr) {
    return executeScript(expr);
}

// ============================================================================
// Skill Handler
// ============================================================================

async function handler(input) {
    if (!input?.input) {
        return { status: 'error', result: 'No input provided. Usage: get:<stateID>, set:<stateID>?value=<value>, etc.' };
    }
    
    const inputStr = String(input.input).trim();
    
    // Parse command
    const colonIndex = inputStr.indexOf(':');
    if (colonIndex === -1) {
        return { 
            status: 'error', 
            result: 'Invalid format. Use: <command>:<stateID>?<params>\n\nCommands: get, set, getBulk, objects, states, search, query, enums, folders, subscribe, toggle, setBulk, create, exec, eval' 
        };
    }
    
    const command = inputStr.substring(0, colonIndex).toLowerCase();
    const rest = inputStr.substring(colonIndex + 1);
    
    try {
        switch (command) {
            case 'get':
                return await getState(rest);
            
            case 'getplainvalue':
                const [gpStateId, ...gpParts] = rest.split('?');
                const gpOptions = {};
                if (gpParts.length) {
                    gpParts.join('?').split('&').forEach(p => {
                        const [k, v] = p.split('=');
                        gpOptions[k] = v;
                    });
                }
                return await getPlainValue(gpStateId, gpOptions);
            
            case 'getbulk':
                return await getBulk(rest);
            
            case 'objects':
                const [objPattern, ...objParts] = rest.split('?');
                const objOptions = {};
                if (objParts.length) {
                    objParts.join('?').split('&').forEach(p => {
                        const [k, v] = p.split('=');
                        objOptions[k] = v;
                    });
                }
                return await getObjects(objPattern, objOptions);
            
            case 'states':
                return await getStates(rest);
            
            case 'search':
                return await searchDataPoints(rest);
            
            case 'query':
                const [queryStateId, ...queryParts] = rest.split('?');
                const queryOptions = {};
                if (queryParts.length) {
                    queryParts.join('?').split('&').forEach(p => {
                        const [k, v] = p.split('=');
                        queryOptions[k] = v;
                    });
                }
                return await queryHistory(queryStateId, queryOptions);
            
            case 'enums':
                return await getEnums();
            
            case 'folders':
                return await getFolders();
            
            case 'subscribe':
                return await subscribeState(rest);
            
            case 'set':
                const [setStateId, ...setParts] = rest.split('?');
                const setOptions = {};
                if (setParts.length) {
                    setParts.join('?').split('&').forEach(p => {
                        const [k, v] = p.split('=');
                        setOptions[k] = v;
                    });
                }
                return await setState(setStateId, setOptions.value, setOptions);
            
            case 'toggle':
                return await toggleState(rest);
            
            case 'setbulk':
                return await setBulk(rest);
            
            case 'create':
                const [createStateId, ...createParts] = rest.split('?');
                const createOptions = { common: {}, native: {} };
                if (createParts.length) {
                    createParts.join('?').split('&').forEach(p => {
                        const [k, v] = p.split('=');
                        if (k === 'common' || k === 'native') {
                            try {
                                createOptions[k] = JSON.parse(v);
                            } catch {
                                createOptions[k] = {};
                            }
                        } else {
                            createOptions[k] = v;
                        }
                    });
                }
                return await createState(createStateId, createOptions.common, createOptions.native);
            
            case 'exec':
                return await executeScript(rest);
            
            case 'eval':
                return await evalExpression(rest);
            
            case 'help':
                return {
                    result: `🎛️ ioBroker Simple-API Skill

Commands:
  get:<stateID>                    Get state + object
  getPlainValue:<stateID>?json    Get value (optional JSON parse)
  getBulk:<id1,id2>               Get multiple states
  objects:<pattern>?type=device   List objects
  states:<pattern>                 List states
  search:<pattern>                 Search data points
  query:<id>?dateFrom=-1h         Query history
  enums                           List enums
  folders                         List folders
  subscribe:<stateID>              Long-poll for changes
  set:<id>?value=1&ack=true       Set state value
  toggle:<id>                      Toggle boolean/number
  setBulk:id1=val1&id2=val2        Bulk set
  create:<id>?common={"name":"x"} Create state
  exec:<js>                       Execute JavaScript
  eval:<expr>                     Quick eval

Config: Set url/port/username/password in openclaw.json under skills.entries.iobroker-simple-api.config`
                };
            
            default:
                return { status: 'error', result: `Unknown command: ${command}` };
        }
    } catch (error) {
        return { status: 'error', result: error.message };
    }
}

// ============================================================================
// Exports
// ============================================================================

module.exports = { handler };
module.exports.handler = handler;
module.exports.default = handler;