import fs from "fs"
import path from "path"

import { astScan } from "./ast_scanner.js"
import { keywordScan } from "./keyword_scanner.js"

export function scanSkill(dir: string, policy: any, patterns: any) {

    const files = fs.readdirSync(dir)

    let results: any[] = []

    for (const file of files) {

        if (!file.endsWith(".ts") && !file.endsWith(".js")) continue

        const full = path.join(dir, file)

        const code = fs.readFileSync(full, "utf8")

        const astIssues = astScan(code, policy)

        const keywordIssues = keywordScan(code, patterns)

        const issues = [...astIssues, ...keywordIssues]

        if (issues.length) {

            results.push({
                file,
                issues
            })

        }

    }

    return {
        safe: results.length === 0,
        results
    }

}