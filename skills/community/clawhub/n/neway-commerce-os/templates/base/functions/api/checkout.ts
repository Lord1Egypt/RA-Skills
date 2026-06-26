export default async function handler(request: Request) {
  const body = await request.json().catch(() => ({}));

  return Response.json({
    ok: true,
    checkoutId: "mock_checkout_session_001",
    mode: body?.paymentMode || "mock",
    items: body?.items || [],
    message: "Checkout scaffold is active. Replace with Stripe session creation for production."
  });
}
