exports.search_products = async function ({ query }) {
  const response = await fetch("https://your-n8n-webhook-url", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ query })
  });

  if (!response.ok) {
    throw new Error("Webhook request failed");
  }

  return await response.json();
};
