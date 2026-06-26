import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { z } from "zod";
import { Octokit } from "@octokit/rest";
import * as dotenv from "dotenv";

dotenv.config();

const REPO_OWNER = "zxz0119";
const REPO_NAME = "NexSolve-AI";

const server = new McpServer({
  name: "NexSolve AI Official Skill",
  version: "1.0.0",
});

const getOctokit = () => {
  const token = process.env.GITHUB_TOKEN;
  if (!token) throw new Error("Missing GITHUB_TOKEN");
  return new Octokit({ auth: token });
};

/**
 * 工具 1: 提交痛点
 */
server.tool(
  "submit_pain_point",
  {
    industry: z.string().describe("行业/Industry"),
    problem: z.string().describe("描述/Problem"),
    contact: z.string().optional().describe("联系方式/Contact"),
  },
  async ({ industry, problem, contact }: { industry: string; problem: string; contact?: string }) => {
    const octokit = getOctokit();
    const issueBody = `
### 提交须知 / Submission Terms
- [x] 我理解本项目仅作为撮合平台。 / I understand the terms.
- [x] 我理解我的需求描述将以 AGPL-3.0 协议公开。 / AGPL-3.0 License.

### 所属行业 / Industry
${industry}

### 痛点描述 / Problem Description
${problem}

### 联系方式 (选填) / Contact Info (Optional)
${contact || "未提供 / Not provided"}
    `;

    const res = await octokit.issues.create({
      owner: REPO_OWNER,
      repo: REPO_NAME,
      title: `【需求】${industry}：${problem.slice(0, 20)}...`,
      body: issueBody,
      labels: ["pain-point", "needs-triage"],
    });
    return { content: [{ type: "text", text: `✅ Created: #${res.data.number}` }] };
  }
);

/**
 * 工具 2: 列表获取
 */
server.tool(
  "list_active_needs",
  { limit: z.number().default(10) },
  async ({ limit }: { limit: number }) => {
    const octokit = getOctokit();
    const { data } = await octokit.issues.listForRepo({
      owner: REPO_OWNER, repo: REPO_NAME, labels: "pain-point", state: "open", per_page: limit
    });
    const text = data.map(i => `[#${i.number}] ${i.title}`).join("\n");
    return { content: [{ type: "text", text: text || "Square is empty." }] };
  }
);

/**
 * 工具 3: 详情获取
 */
server.tool(
  "get_need_detail",
  { id: z.number() },
  async ({ id }: { id: number }) => {
    const octokit = getOctokit();
    const { data } = await octokit.issues.get({
      owner: REPO_OWNER, repo: REPO_NAME, issue_number: id
    });
    return { content: [{ type: "text", text: `Title: ${data.title}\nBody:\n${data.body}` }] };
  }
);

const transport = new StdioServerTransport();
await server.connect(transport);