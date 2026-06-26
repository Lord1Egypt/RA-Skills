export default async function handler(request: Request) {
  const signature = request.headers.get("stripe-signature");

  return Response.json({
    ok: true,
    received: true,
    signaturePresent: Boolean(signature),
    message: "Stripe webhook scaffold is active. Replace with signature verification and event processing for production."
  });
}
