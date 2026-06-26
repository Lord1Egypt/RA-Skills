"use strict";
// Micro Memory - Utility Functions
var __createBinding = (this && this.__createBinding) || (Object.create ? (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    var desc = Object.getOwnPropertyDescriptor(m, k);
    if (!desc || ("get" in desc ? !m.__esModule : desc.writable || desc.configurable)) {
      desc = { enumerable: true, get: function() { return m[k]; } };
    }
    Object.defineProperty(o, k2, desc);
}) : (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    o[k2] = m[k];
}));
var __setModuleDefault = (this && this.__setModuleDefault) || (Object.create ? (function(o, v) {
    Object.defineProperty(o, "default", { enumerable: true, value: v });
}) : function(o, v) {
    o["default"] = v;
});
var __importStar = (this && this.__importStar) || (function () {
    var ownKeys = function(o) {
        ownKeys = Object.getOwnPropertyNames || function (o) {
            var ar = [];
            for (var k in o) if (Object.prototype.hasOwnProperty.call(o, k)) ar[ar.length] = k;
            return ar;
        };
        return ownKeys(o);
    };
    return function (mod) {
        if (mod && mod.__esModule) return mod;
        var result = {};
        if (mod != null) for (var k = ownKeys(mod), i = 0; i < k.length; i++) if (k[i] !== "default") __createBinding(result, mod, k[i]);
        __setModuleDefault(result, mod);
        return result;
    };
})();
Object.defineProperty(exports, "__esModule", { value: true });
exports.ARCHIVE_DIR = exports.STORE_FILE = exports.REVIEWS_FILE = exports.LINKS_FILE = exports.INDEX_FILE = exports.STORE_DIR = void 0;
exports.ensureDir = ensureDir;
exports.readJson = readJson;
exports.writeJson = writeJson;
exports.formatTimestamp = formatTimestamp;
exports.parseTimestamp = parseTimestamp;
exports.daysBetween = daysBetween;
exports.getStrengthLevel = getStrengthLevel;
exports.getStrengthColor = getStrengthColor;
exports.resetColor = resetColor;
exports.printColored = printColored;
exports.truncate = truncate;
exports.fuzzyMatch = fuzzyMatch;
const fs = __importStar(require("fs"));
const path = __importStar(require("path"));
exports.STORE_DIR = path.join(__dirname, '..', 'store');
exports.INDEX_FILE = path.join(exports.STORE_DIR, 'index.json');
exports.LINKS_FILE = path.join(exports.STORE_DIR, 'links.json');
exports.REVIEWS_FILE = path.join(exports.STORE_DIR, 'reviews.json');
exports.STORE_FILE = path.join(exports.STORE_DIR, 'store.md');
exports.ARCHIVE_DIR = path.join(exports.STORE_DIR, 'archive');
function ensureDir(dir) {
    if (!fs.existsSync(dir)) {
        fs.mkdirSync(dir, { recursive: true });
    }
}
function readJson(filePath, defaultValue) {
    try {
        if (fs.existsSync(filePath)) {
            const data = fs.readFileSync(filePath, 'utf-8');
            return JSON.parse(data);
        }
    }
    catch (e) {
        console.error(`Error reading ${filePath}:`, e);
    }
    return defaultValue;
}
function writeJson(filePath, data) {
    ensureDir(path.dirname(filePath));
    fs.writeFileSync(filePath, JSON.stringify(data, null, 2), 'utf-8');
}
function formatTimestamp(date = new Date()) {
    const pad = (n) => n.toString().padStart(2, '0');
    return `${date.getFullYear()}-${pad(date.getMonth() + 1)}-${pad(date.getDate())} ${pad(date.getHours())}:${pad(date.getMinutes())}`;
}
function parseTimestamp(ts) {
    return new Date(ts.replace(' ', 'T'));
}
function daysBetween(date1, date2) {
    const msPerDay = 24 * 60 * 60 * 1000;
    return Math.floor((date2.getTime() - date1.getTime()) / msPerDay);
}
function getStrengthLevel(score) {
    if (score >= 80)
        return 'permanent';
    if (score >= 60)
        return 'strong';
    if (score >= 40)
        return 'stable';
    if (score >= 20)
        return 'weak';
    return 'critical';
}
function getStrengthColor(level) {
    const colors = {
        permanent: '\x1b[35m', // magenta
        strong: '\x1b[32m', // green
        stable: '\x1b[36m', // cyan
        weak: '\x1b[33m', // yellow
        critical: '\x1b[31m', // red
    };
    return colors[level] || '\x1b[0m';
}
function resetColor() {
    return '\x1b[0m';
}
function printColored(text, color) {
    const colorCodes = {
        cyan: '\x1b[36m',
        green: '\x1b[32m',
        yellow: '\x1b[33m',
        red: '\x1b[31m',
        gray: '\x1b[90m',
    };
    console.log(`${colorCodes[color] || ''}${text}${resetColor()}`);
}
function truncate(str, maxLength) {
    if (str.length <= maxLength)
        return str;
    return str.substring(0, maxLength - 3) + '...';
}
function fuzzyMatch(text, keyword) {
    const normalizedText = text.toLowerCase();
    const normalizedKeyword = keyword.toLowerCase();
    return normalizedText.includes(normalizedKeyword);
}
//# sourceMappingURL=utils.js.map