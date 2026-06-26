import OpenAI from "openai";

const client = new OpenAI();
const BASE = "https://happythoughts.proteeninjector.workers.dev";

const tools = [
  {
    type: "function",
    function: {
      name: "discover_providers",
      description: "Browse available Happy Thoughts providers by specialty.",
      parameters: {
        type: "object",
        properties: {
          specialty: {
            type: "string",
            description: "Optional parent or leaf specialty such as trading or trading/signals"
          }
        }
      }
    }
  },
  {
    type: "function",
    function: {
      name: "preview_route",
      description: "Preview top providers without paying.",
      parameters: {
        type: "object",
        properties: {
          specialty: {
            type: "string",
            description: "Optional specialty such as trading/signals"
          }
        }
      }
    }
  }
];

async function executeToolCall(name, args) {
  if (name === "discover_providers") {
    const url = args.specialty
      ? `${BASE}/discover?specialty=${encodeURIComponent(args.specialty)}`
      : `${BASE}/discover`;
    const res = await fetch(url);
    return JSON.stringify(await res.json());
  }

  if (name === "preview_route") {
    const url = args.specialty
      ? `${BASE}/route?specialty=${encodeURIComponent(args.specialty)}`
      : `${BASE}/route`;
    const res = await fetch(url);
    return JSON.stringify(await res.json());
  }

  throw new Error(`Unknown tool: ${name}`);
}

async function runAgent(userMessage) {
  const messages = [
    {
      role: "system",
      content:
        "You have read-only discovery access to Happy Thoughts. Use the tools to inspect providers and preview routing."
    },
    { role: "user", content: userMessage }
  ];

  while (true) {
    const response = await client.chat.completions.create({
      model: "gpt-4o",
      messages,
      tools,
      tool_choice: "auto"
    });

    const message = response.choices[0].message;
    messages.push(message);

    if (!message.tool_calls?.length) {
      return message.content;
    }

    for (const toolCall of message.tool_calls) {
      const args = JSON.parse(toolCall.function.arguments);
      const result = await executeToolCall(toolCall.function.name, args);
      messages.push({ role: "tool", tool_call_id: toolCall.id, content: result });
    }
  }
}

const answer = await runAgent(
  "Show me the currently live trading-related providers on Happy Thoughts and preview routing for trading/signals."
);

console.log(answer);
