#!/usr/bin/env node

import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { z } from "zod";
import * as fs from "fs";
import * as path from "path";
import * as os from "os";
import { parse } from "csv-parse/sync";
import * as https from "https";

const SDN_URL = process.env.SDN_URL || "https://www.treasury.gov/ofac/downloads/sdn.csv";
const CACHE_FILE = path.join(os.tmpdir(), "ofac-sdn-cache.csv");
const CACHE_MAX_AGE_MS = 24 * 60 * 60 * 1000; // 24 hours

interface SDNEntry {
  ent_num: string;
  name: string;
  type: string;
  programs: string;
  title: string;
  remarks: string;
}

function downloadFile(url: string, dest: string): Promise<void> {
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
      if (response.statusCode && response.statusCode !== 200) {
        file.close();
        fs.unlink(dest, () => {});
        reject(new Error(`HTTP request failed with status code ${response.statusCode}`));
        return;
      }
      response.pipe(file);
      file.on("finish", () => {
        file.close();
        resolve();
      });
    }).on("error", (err) => {
      fs.unlink(dest, () => {});
      reject(err);
    });
  });
}

async function getSDNData(): Promise<SDNEntry[]> {
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
  const records = parse(csvContent, {
    relax_column_count: true,
    skip_empty_lines: true,
  }) as string[][];

  return records.map((row) => ({
    ent_num: row[0] || "",
    name: row[1] || "",
    type: row[2] || "",
    programs: row[3] || "",
    title: row[4] || "",
    remarks: row[11] || "",
  }));
}

function searchEntries(
  entries: SDNEntry[],
  name: string,
  country?: string
): SDNEntry[] {
  const nameLower = name.toLowerCase();
  const nameTokens = nameLower.split(/\s+/);

  return entries.filter((entry) => {
    const entryName = entry.name.toLowerCase();

    // Check if all tokens of the search name appear in the entry name
    const nameMatch = nameTokens.every((token) => entryName.includes(token));
    if (!nameMatch) return false;

    if (country) {
      const countryLower = country.toLowerCase();
      const remarksLower = entry.remarks.toLowerCase();
      if (!remarksLower.includes(countryLower)) return false;
    }

    return true;
  });
}

const server = new McpServer({
  name: "sanctions-check",
  version: "1.0.0",
});

server.tool(
  "check_sanctions",
  "Check a name against the OFAC SDN (Specially Designated Nationals) sanctions list. Returns matching entries if found.",
  {
    name: z.string().min(1).describe("The name to check against the sanctions list"),
    country: z
      .string()
      .optional()
      .describe("Optional country to narrow the search"),
  },
  async ({ name, country }) => {
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
            type: "text" as const,
            text: JSON.stringify(result, null, 2),
          },
        ],
      };
    } catch (error) {
      const message = error instanceof Error ? error.message : String(error);
      return {
        content: [
          {
            type: "text" as const,
            text: JSON.stringify({
              error: `Failed to check sanctions: ${message}`,
              checked_at: new Date().toISOString(),
            }),
          },
        ],
        isError: true,
      };
    }
  }
);

async function main() {
  const transport = new StdioServerTransport();
  await server.connect(transport);
}

main().catch((error) => {
  console.error("Server error:", error);
  process.exit(1);
});
