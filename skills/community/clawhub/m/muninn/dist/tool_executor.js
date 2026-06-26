import { McpError, ErrorCode } from "@modelcontextprotocol/sdk/types.js";
import { ProjectManager } from "./project_manager.js";
import * as path from "path";
import fs from "fs-extra";
export class ToolExecutor {
    projectManager;
    constructor(projectManager) {
        this.projectManager = projectManager;
    }
    async execute(name, args) {
        switch (name) {
            case "init_project":
                return this.handleInitProject(args);
            case "brain_check":
                return this.handleBrainCheck(args);
            case "add_memory":
                return this.handleAddMemory(args);
            case "search_context":
                return this.handleSearchContext(args);
            case "reindex_context":
                return this.handleReindexContext(args);
            case "enforce_rules":
                return this.handleEnforceRules(args);
            case "filesystem_write_test":
                return { content: [{ type: "text", text: `Successfully wrote to ${args.path} (SIMULATED)` }] };
            default:
                throw new McpError(ErrorCode.MethodNotFound, `Unknown tool: ${name}`);
        }
    }
    async handleInitProject(args) {
        const projectPath = args.project_path || process.cwd();
        const absolutePath = path.resolve(projectPath);
        if (await this.projectManager.isInitialized(absolutePath)) {
            return { content: [{ type: "text", text: `Project already initialized at ${absolutePath}/.muninn/` }] };
        }
        await this.projectManager.initProject(absolutePath);
        await this.projectManager.setActiveProject(absolutePath);
        await this.projectManager.indexProject(absolutePath);
        return { content: [{ type: "text", text: "Muninn initialized successfully!" }] };
    }
    async handleBrainCheck(args) {
        const currentProject = this.projectManager.getCurrentProject();
        if (!currentProject)
            return { content: [{ type: "text", text: "⚠️ No active project. Run reindex_context first." }] };
        const context = await this.projectManager.searchContext(args.task_description, 3);
        return {
            content: [{
                    type: "text",
                    text: `🧠 **BRAIN CHECK COMPLETE**\n\nProject: ${path.basename(currentProject)}\n\n${context}\n\n✅ Context loaded.`
                }]
        };
    }
    async handleAddMemory(args) {
        const filePath = await this.projectManager.addMemory(args.title, args.content, args.category);
        return { content: [{ type: "text", text: `Memory saved to: ${filePath}` }] };
    }
    async handleSearchContext(args) {
        const result = await this.projectManager.searchContext(args.query, args.limit || 5);
        return { content: [{ type: "text", text: result }] };
    }
    async handleReindexContext(args) {
        const projectPath = args.project_path || process.cwd();
        const absolutePath = path.resolve(projectPath);
        await this.projectManager.setActiveProject(absolutePath);
        await this.projectManager.indexProject(absolutePath);
        return { content: [{ type: "text", text: "Project re-indexed." }] };
    }
    async handleEnforceRules(args) {
        const projectPath = args.project_path || this.projectManager.getCurrentProject();
        if (!projectPath)
            throw new Error("No active project detected.");
        const updated = await this.projectManager.ensureRules(projectPath, true);
        return { content: [{ type: "text", text: `Rules enforced for: ${updated.join(', ') || 'none'}` }] };
    }
}
