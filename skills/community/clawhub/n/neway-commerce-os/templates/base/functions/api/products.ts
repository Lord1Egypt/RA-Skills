export default async function handler() {
  return Response.json({
    ok: true,
    products: [
      {
        id: "ui-kit-pro",
        name: "UI Kit Pro",
        price: 79,
        category: "design",
        tagline: "Premium components and sections for fast launches."
      },
      {
        id: "ai-workflow-pack",
        name: "AI Workflow Pack",
        price: 129,
        category: "ai",
        tagline: "Reusable prompts, automations, and workflow recipes."
      },
      {
        id: "creator-launch-box",
        name: "Creator Launch Box",
        price: 149,
        category: "growth",
        tagline: "Landing pages, funnel copy, and launch assets."
      }
    ]
  });
}
