#!/usr/bin/env node
"use strict";
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
const mcp_js_1 = require("@modelcontextprotocol/sdk/server/mcp.js");
const stdio_js_1 = require("@modelcontextprotocol/sdk/server/stdio.js");
const zod_1 = require("zod");
const fs = __importStar(require("fs"));
const path = __importStar(require("path"));
const os = __importStar(require("os"));
const sync_1 = require("csv-parse/sync");
const https = __importStar(require("https"));
const SDN_URL = "https://www.treasury.gov/ofac/downloads/sdn.csv";
const CACHE_FILE = path.join(os.tmpdir(), "ofac-sdn-cache.csv");
const CACHE_MAX_AGE_MS = 24 * 60 * 60 * 1000; // 24 hours
function downloadFile(url, dest) {
    return new Promise((resolve, reject) => {
        const file = fs.createWriteStream(dest);
        https.get(url, (response) => {
            if (response.statusCode === 301 || response.statusCode === 302) {
                const redirectUrl = response.headers.location;
                if (redirectUrl) {
                    file.close();
                    fs.unlinkSync(dest);
                    downloadFile(redirectUrl, dest).then(resolve, reject);
                    return;
                }
            }
            response.pipe(file);
            file.on("finish", () => {
                file.close();
                resolve();
            });
        }).on("error", (err) => {
            fs.unlink(dest, () => { });
            reject(err);
        });
    });
}
async function getSDNData() {
    let needsDownload = true;
    if (fs.existsSync(CACHE_FILE)) {
        const stats = fs.statSync(CACHE_FILE);
        const age = Date.now() - stats.mtimeMs;
        if (age < CACHE_MAX_AGE_MS) {
            needsDownload = false;
        }
    }
    if (needsDownload) {
        await downloadFile(SDN_URL, CACHE_FILE);
    }
    const csvContent = fs.readFileSync(CACHE_FILE, "utf-8");
    const records = (0, sync_1.parse)(csvContent, {
        relax_column_count: true,
        skip_empty_lines: true,
    });
    return records.map((row) => ({
        ent_num: row[0] || "",
        name: row[1] || "",
        type: row[2] || "",
        programs: row[3] || "",
        title: row[4] || "",
        remarks: row[11] || "",
    }));
}
function searchEntries(entries, name, country) {
    const nameLower = name.toLowerCase();
    const nameTokens = nameLower.split(/\s+/);
    return entries.filter((entry) => {
        const entryName = entry.name.toLowerCase();
        // Check if all tokens of the search name appear in the entry name
        const nameMatch = nameTokens.every((token) => entryName.includes(token));
        if (!nameMatch)
            return false;
        if (country) {
            const countryLower = country.toLowerCase();
            const remarksLower = entry.remarks.toLowerCase();
            if (!remarksLower.includes(countryLower))
                return false;
        }
        return true;
    });
}
const server = new mcp_js_1.McpServer({
    name: "sanctions-check",
    version: "1.0.0",
});
server.tool("check_sanctions", "Check a name against the OFAC SDN (Specially Designated Nationals) sanctions list. Returns matching entries if found.", {
    name: zod_1.z.string().describe("The name to check against the sanctions list"),
    country: zod_1.z
        .string()
        .optional()
        .describe("Optional country to narrow the search"),
}, async ({ name, country }) => {
    try {
        const entries = await getSDNData();
        const matches = searchEntries(entries, name, country);
        const result = {
            match: matches.length > 0,
            entries: matches.map((m) => ({
                name: m.name,
                type: m.type,
                programs: m.programs,
                remarks: m.remarks,
            })),
            checked_at: new Date().toISOString(),
        };
        return {
            content: [
                {
                    type: "text",
                    text: JSON.stringify(result, null, 2),
                },
            ],
        };
    }
    catch (error) {
        const message = error instanceof Error ? error.message : String(error);
        return {
            content: [
                {
                    type: "text",
                    text: JSON.stringify({
                        error: `Failed to check sanctions: ${message}`,
                        checked_at: new Date().toISOString(),
                    }),
                },
            ],
            isError: true,
        };
    }
});
async function main() {
    const transport = new stdio_js_1.StdioServerTransport();
    await server.connect(transport);
}
main().catch((error) => {
    console.error("Server error:", error);
    process.exit(1);
});
//# sourceMappingURL=index.js.map