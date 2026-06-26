import fs from "fs"
import path from "path"
import url from "url"
import { scanSkill } from "./scanner/skill_scanner.js"
import { aiReview } from "./llm/ai_review.js"

// ESM alternative to __dirname
const __dirname = path.dirname(url.fileURLToPath(import.meta.url))

export default {

    id: "security_suite",

    description: "Unified openclaw security suite for static scanning and semantic review",

    async run({ action, path: targetPath }: any, ctx: any) {

        if (action === "scan") {

            const policy = JSON.parse(
                fs.readFileSync(path.join(__dirname, "config/policy.json"), "utf8")
            )

            const patterns = JSON.parse(
                fs.readFileSync(path.join(__dirname, "config/malicious_patterns.json"), "utf8")
            )

            return scanSkill(targetPath, policy, patterns)

        } else if (action === "review") {

            if (!fs.existsSync(targetPath)) {
                throw new Error(`File not found: ${targetPath}`)
            }

            const code = fs.readFileSync(targetPath, "utf8")

            if (!ctx || !ctx.llm) {
                throw new Error("LLM context (ctx.llm) is required for semantic review.")
            }

            return aiReview(code, ctx.llm)

        } else {
            throw new Error(`Unknown action: ${action}. Expected 'scan' or 'review'.`)
        }

    }

}