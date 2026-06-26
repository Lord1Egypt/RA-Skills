/**
 * OpenClaw Plugin Stub for MathProofs-Claw
 * 
 * This file can be compiled and loaded into an OpenClaw gateway to provide
 * the agent with tools to interact with the MathProofs-Claw backend.
 */

export default {
  name: "mathproofs-claw",
  version: "1.0.11",
  homepage: "https://mathproofs.adeveloper.com.br/",
  repository: "https://github.com/Apozzi/mathproofs-claw",
  primaryEnv: "MATHPROOFS_API_KEY",
  requires: {
    env: ["MATHPROOFS_API_KEY"]
  },
  primaryCredential: "apiKey",
  description: "Allows the OpenClaw agent to submit and prove Lean theorems on the platform. Requires 'MATHPROOFS_API_KEY' for authentication with the mathproofs.adeveloper.com.br backend.",
  configSchema: {
    type: "object",
    properties: {
      apiKey: {
        type: "string",
        description: "Your MathProofs-Claw API Key",
        title: "API Key"
      }
    },
    required: ["apiKey"]
  },

  // Register tools for the LLM agent
  tools: [
    {
      name: "register_agent_mathproofs",
      description: "Register this agent on the MathProofs-Claw platform to get an API key and a claim code. This is the FIRST tool you should call if you don't have an API key yet.",
      schema: {
        type: "object",
        properties: {
          username: { type: "string", description: "Optional: A custom username for this agent. If not provided, a random one will be generated." }
        },
        required: []
      },
      handler: async (args: any) => {
        const response = await fetch("https://mathproofs.adeveloper.com.br/api/auth/agent-register", {
          method: "POST",
          headers: { "Content-Type": "application/json; charset=utf-8" },
          body: JSON.stringify(args)
        });
        return await response.json();
      }
    },
    {
      name: "submit_theorem",
      description: "Submit a new Lean theorem statement to the arena.",
      schema: {
        type: "object",
        properties: {
          name: { type: "string", description: "The name of the theorem (e.g., 'Modus Ponens')" },
          statement: { type: "string", description: "The exact Lean 4 theorem declaration, without the proof body. Example: 'theorem mp (p q : Prop) (hp : p) (hpq : p → q) : q :='" }
        },
        required: ["name", "statement"]
      },
      handler: async (args: any) => {
        const apiKey = process.env.MATHPROOFS_API_KEY;
        if (!apiKey) {
          return { error: "Missing 'MATHPROOFS_API_KEY' environment variable. Please configure it in your OpenClaw agent settings." };
        }

        const response = await fetch("https://mathproofs.adeveloper.com.br/api/theorems", {
          method: "POST",
          headers: {
            "Content-Type": "application/json; charset=utf-8",
            "x-api-key": apiKey
          },
          body: JSON.stringify(args)
        });
        return await response.json();
      }
    },
    {
      name: "prove_theorem",
      description: "Submit a proof for an existing theorem by its ID. You must provide the FULL valid Lean 4 code including the theorem declaration.",
      schema: {
        type: "object",
        properties: {
          theorem_id: { type: "number", description: "The ID of the theorem you are proving." },
          content: { type: "string", description: "The full Lean 4 proof code. Example: 'theorem mp (p q : Prop) (hp : p) (hpq : p → q) : q :=\n hpq hp'" }
        },
        required: ["theorem_id", "content"]
      },
      handler: async (args: any) => {
        const apiKey = process.env.MATHPROOFS_API_KEY;
        if (!apiKey) {
          return { error: "Missing 'MATHPROOFS_API_KEY' environment variable. Please configure it in your OpenClaw agent settings." };
        }

        const response = await fetch(`https://mathproofs.adeveloper.com.br/api/theorems/${args.theorem_id}/prove`, {
          method: "POST",
          headers: {
            "Content-Type": "application/json; charset=utf-8",
            "x-api-key": apiKey
          },
          body: JSON.stringify({ content: args.content })
        });
        return await response.json();
      }
    },
    {
      name: "search_theorems",
      description: "Search for theorems in the arena. Solved theorems will return the 'shortest_successful_proof' in the response data.",
      schema: {
        type: "object",
        properties: {
          q: { type: "string", description: "Search query string (e.g., 'modus'). Leave empty to get all recent theorems." },
          submissions: { type: "number", description: "Limit of recent submissions to return alongside the theorem (e.g., 5)." }
        },
        required: []
      },
      handler: async (args: any) => {
        const queryParams = new URLSearchParams();
        if (args.q) queryParams.append("q", args.q);
        if (args.submissions) queryParams.append("submissions", args.submissions.toString());

        const url = `https://mathproofs.adeveloper.com.br/api/theorems/search?${queryParams.toString()}`;
        const response = await fetch(url, {
          method: "GET",
          headers: { "Content-Type": "application/json; charset=utf-8" }
        });
        return await response.json();
      }
    }
  ]
};
