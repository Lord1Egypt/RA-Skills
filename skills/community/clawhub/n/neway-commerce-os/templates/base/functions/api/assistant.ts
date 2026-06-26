type ChatMessage = {
  role?: "user" | "assistant" | "system";
  content?: string;
};

function buildReply(messages: ChatMessage[]) {
  const lastUserMessage =
    [...messages].reverse().find((message) => message.role === "user")?.content?.toLowerCase() || "";

  if (lastUserMessage.includes("design") || lastUserMessage.includes("ui")) {
    return "For design speed and premium presentation, I recommend UI Kit Pro first. It gives you the fastest path to a polished storefront.";
  }

  if (lastUserMessage.includes("ai") || lastUserMessage.includes("automation")) {
    return "If your goal is automation or reusable AI systems, start with AI Workflow Pack. It’s the best fit for process leverage and repeatability.";
  }

  if (lastUserMessage.includes("launch") || lastUserMessage.includes("growth")) {
    return "For launch planning, funnel assets, and creator monetization, Creator Launch Box is the strongest starting point.";
  }

  return "I’d start with UI Kit Pro for fast launch quality, or AI Workflow Pack if you want automation leverage. Tell me your budget or use case and I’ll narrow it down.";
}

export default async function handler(request: Request) {
  const body = await request.json().catch(() => ({}));
  const messages = Array.isArray(body?.messages) ? body.messages : [];

  return Response.json({
    ok: true,
    reply: buildReply(messages),
    recommendedProductIds: ["ui-kit-pro", "ai-workflow-pack"],
    cta: "Add recommended product to cart"
  });
}
