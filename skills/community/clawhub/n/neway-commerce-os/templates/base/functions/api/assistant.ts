// AI shopping assistant endpoint (scaffold).
// To go live: set AI_API_BASE / AI_API_KEY / AI_MODEL in the environment and forward
// the messages to that provider. Until then this returns a keyword-based mock reply
// that mirrors the front-end widget in `src/components/AIChatWidget.tsx`.

type ChatMessage = {
  role?: 'user' | 'assistant' | 'system';
  content?: string;
};

function has(text: string, keywords: string[]): boolean {
  return keywords.some((k) => text.includes(k));
}

function buildReply(messages: ChatMessage[]): string {
  const last =
    [...messages].reverse().find((message) => message.role === 'user')?.content?.toLowerCase() || '';

  if (has(last, ['gift', 'present', 'for her', 'for him'])) {
    return 'For a gift I would look at the silk twill scarf and the combed cotton tee first — friendly on price, arrives boxed, hard to get wrong.';
  }
  if (has(last, ['new', 'latest', 'arrival', 'just in'])) {
    return 'Among the new arrivals, the wool-blend long coat and the silk floral dress have had the best feedback, and the size runs are still complete.';
  }
  if (has(last, ['sale', 'discount', 'deal', 'offer'])) {
    return 'On promotion right now: the vintage biker jacket, the quilted chain bag and the silk twill scarf. Stock is limited on all three.';
  }
  if (has(last, ['size', 'fit', 'sizing'])) {
    return 'Everything runs true to size overall. Tailored outerwear is worth taking one size up; knitwear and tees are fine at your usual size.';
  }
  return 'Tell me the occasion and your budget and I will narrow it down to two or three specific pieces.';
}

export default async function handler(request: Request) {
  const body = await request.json().catch(() => ({}));
  const messages = Array.isArray(body?.messages) ? (body.messages as ChatMessage[]) : [];

  return Response.json({
    ok: true,
    source: 'mock',
    reply: buildReply(messages),
    recommendedProductIds: ['wool-blend-coat', 'silk-floral-dress'],
    cta: 'Add the recommendations to cart',
  });
}
