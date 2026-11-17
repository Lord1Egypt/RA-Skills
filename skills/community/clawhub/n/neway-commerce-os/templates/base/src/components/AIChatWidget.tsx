import { useEffect, useRef, useState } from 'react';
import { Link } from 'react-router-dom';
import { Send, ShoppingBag, Sparkles, X } from 'lucide-react';
import { products } from '../data/products';
import { Product } from '../types';
import { formatPrice } from '../utils/format';
import clsx from 'clsx';

interface Message {
  role: 'user' | 'assistant';
  content: string;
  products?: Product[];
}

const suggestions = [
  'What should I wear to the office',
  'Find me a gift under ¥500',
  'What just arrived',
  'How do I pick a size',
];

const BRAND = '__BRAND_NAME__';

/** Matches when any keyword appears in the message. */
function matches(text: string, keywords: string[]): boolean {
  return keywords.some((k) => text.includes(k));
}

function byRating(count = 3): Product[] {
  return [...products].sort((a, b) => b.rating - a.rating).slice(0, count);
}

/**
 * 10 keyword scenarios plus a default. Extend this list to match the brand voice —
 * each branch returns a line of copy and a set of product cards.
 */
function mockAIResponse(input: string): { content: string; products: Product[] } {
  const text = input.toLowerCase();

  if (matches(text, ['gift', 'present', 'for her', 'for him'])) {
    const budgetMatch = input.match(/(\d+)/);
    const budget = budgetMatch ? Number(budgetMatch[1]) : null;
    const within = budget
      ? products.filter((p) => p.price <= budget).sort((a, b) => b.rating - a.rating).slice(0, 3)
      : [];
    const recs = within.length > 0 ? within : byRating(3);
    return {
      content: `Three safe picks for a gift${budget ? `, all under ${formatPrice(budget)}` : ''}. They arrive boxed, and nobody has sent one back yet:`,
      products: recs,
    };
  }

  if (matches(text, ['new', 'latest', 'arrival', 'just in', 'just arrived'])) {
    return {
      content: 'These just landed and the size run is still complete:',
      products: products.filter((p) => p.isNew),
    };
  }

  if (matches(text, ['sale', 'discount', 'deal', 'offer', 'reduced'])) {
    return {
      content: 'These are on promotion right now, and stock is limited:',
      products: products.filter((p) => p.isSale),
    };
  }

  if (matches(text, ['best', 'popular', 'top', 'bestseller', 'favourite', 'favorite'])) {
    return {
      content: 'The ones people buy again and rate highest — hard to get wrong:',
      products: [...products].sort((a, b) => b.reviewCount - a.reviewCount).slice(0, 4),
    };
  }

  if (matches(text, ['budget', 'price', 'cheap', 'affordable', 'how much'])) {
    const budgetMatch = input.match(/(\d+)/);
    const budget = budgetMatch ? Number(budgetMatch[1]) : 800;
    const recs = products.filter((p) => p.price <= budget).sort((a, b) => b.rating - a.rating).slice(0, 4);
    return {
      content: `Staying under ${formatPrice(budget)}, these give the most for the money:`,
      products: recs,
    };
  }

  if (matches(text, ['premium', 'luxury', 'exclusive', 'high end', 'investment'])) {
    return {
      content: 'If budget is not the first concern, these are the ones worth it on fabric and construction:',
      products: [...products].sort((a, b) => b.price - a.price).slice(0, 3),
    };
  }

  if (matches(text, ['commute', 'work', 'office', 'formal', 'meeting'])) {
    return {
      content: 'For the office I would start with two outerwear pieces and a shirt — they mix furthest:',
      products: products.filter((p) => ['outerwear', 'tops'].includes(p.category)).slice(0, 3),
    };
  }

  if (matches(text, ['date', 'party', 'evening', 'occasion', 'wedding'])) {
    return {
      content: 'For an occasion, a dress and a bag finish the look fastest:',
      products: products.filter((p) => ['dress', 'bags'].includes(p.category)).slice(0, 3),
    };
  }

  if (matches(text, ['size', 'fit', 'sizing', 'true to size'])) {
    return {
      content: `Sizing: ${BRAND} runs true to size overall. Tailored outerwear is worth taking one size up; knitwear and tees are fine at your usual size. These are the looser cuts:`,
      products: products.filter((p) => p.fit.toLowerCase().includes('relaxed')).slice(0, 3),
    };
  }

  if (matches(text, ['material', 'fabric', 'composition', 'care', 'wash'])) {
    return {
      content: 'We only list real composition on the product page. These are the fabrics customers come back for:',
      products: products.filter((p) => ['silk', 'cashmere'].some((m) => p.material.toLowerCase().includes(m))).slice(0, 3),
    };
  }

  return {
    content: `Hi, I am the ${BRAND} shopping assistant. Tell me the occasion, your budget or the style you are after and I will narrow it down.`,
    products: byRating(3),
  };
}

export default function AIChatWidget() {
  const [open, setOpen] = useState(false);
  const [messages, setMessages] = useState<Message[]>([
    {
      role: 'assistant',
      content: `Hi, I am the ${BRAND} shopping assistant. Tell me the style or the occasion and I will find the pieces.`,
    },
  ]);
  const [input, setInput] = useState('');
  const [typing, setTyping] = useState(false);
  const endRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    endRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages, typing]);

  const send = async (text?: string) => {
    const msg = (text || input).trim();
    if (!msg) return;
    setInput('');

    setMessages((m) => [...m, { role: 'user', content: msg }]);
    setTyping(true);

    await new Promise((r) => setTimeout(r, 700 + Math.random() * 500));

    const { content, products: recs } = mockAIResponse(msg);
    setMessages((m) => [...m, { role: 'assistant', content, products: recs }]);
    setTyping(false);
  };

  return (
    <>
      {/* Floating action button */}
      <button
        onClick={() => setOpen(true)}
        className={clsx(
          'fixed bottom-6 right-6 z-40 flex h-14 w-14 items-center justify-center rounded-full bg-brand-600 text-white shadow-2xl transition-all duration-200 hover:scale-110 hover:bg-brand-700',
          open && 'hidden'
        )}
        aria-label="Open the shopping assistant"
      >
        <Sparkles size={22} />
      </button>

      {/* Chat panel */}
      <div
        className={clsx(
          'fixed bottom-6 right-6 z-40 flex w-96 max-h-[600px] origin-bottom-right flex-col rounded-2xl bg-white shadow-2xl transition-all duration-300',
          open ? 'pointer-events-auto scale-100 opacity-100' : 'pointer-events-none scale-90 opacity-0'
        )}
      >
        {/* Header */}
        <div className="flex items-center justify-between rounded-t-2xl bg-brand-600 px-5 py-4">
          <div className="flex items-center gap-2">
            <Sparkles size={16} className="text-white" />
            <span className="text-sm font-medium text-white">Shopping assistant</span>
          </div>
          <button
            onClick={() => setOpen(false)}
            className="text-white/70 transition-colors hover:text-white"
            aria-label="Close the assistant"
          >
            <X size={18} />
          </button>
        </div>

        {/* Messages */}
        <div className="min-h-0 flex-1 space-y-4 overflow-y-auto p-4">
          {messages.map((m, i) => (
            <div key={i} className={clsx('flex', m.role === 'user' ? 'justify-end' : 'justify-start')}>
              <div
                className={clsx(
                  'max-w-[85%] rounded-2xl px-4 py-3 text-sm leading-relaxed',
                  m.role === 'user'
                    ? 'rounded-br-sm bg-brand-600 text-white'
                    : 'rounded-bl-sm bg-neutral-50 text-neutral-800'
                )}
              >
                <p className="whitespace-pre-wrap">{m.content}</p>
                {m.products && m.products.length > 0 && (
                  <div className="mt-3 space-y-2">
                    {m.products.slice(0, 3).map((p) => (
                      <Link
                        key={p.id}
                        to={`/product/${p.id}`}
                        onClick={() => setOpen(false)}
                        className="flex items-center gap-3 rounded-xl border border-neutral-100 bg-white p-2 transition-colors hover:border-brand-300"
                      >
                        <img
                          src={p.images[0]}
                          alt={p.name}
                          className="h-14 w-12 rounded-lg bg-neutral-100 object-cover"
                        />
                        <div className="min-w-0 flex-1">
                          <p className="truncate text-xs font-medium text-neutral-800">{p.name}</p>
                          {p.nameEn && <p className="truncate text-xs text-neutral-400">{p.nameEn}</p>}
                          <div className="mt-1 flex items-center gap-1.5">
                            <span className="text-xs font-semibold text-neutral-900">{formatPrice(p.price)}</span>
                            {p.isNew && (
                              <span className="rounded bg-brand-600 px-1.5 py-0.5 text-[12px] text-white">New</span>
                            )}
                          </div>
                        </div>
                        <ShoppingBag size={14} className="shrink-0 text-neutral-400" />
                      </Link>
                    ))}
                  </div>
                )}
              </div>
            </div>
          ))}
          {typing && (
            <div className="flex justify-start">
              <div className="rounded-2xl rounded-bl-sm bg-neutral-50 px-4 py-3">
                <div className="flex gap-1">
                  <span className="h-2 w-2 animate-bounce rounded-full bg-neutral-400" style={{ animationDelay: '0ms' }} />
                  <span className="h-2 w-2 animate-bounce rounded-full bg-neutral-400" style={{ animationDelay: '150ms' }} />
                  <span className="h-2 w-2 animate-bounce rounded-full bg-neutral-400" style={{ animationDelay: '300ms' }} />
                </div>
              </div>
            </div>
          )}
          <div ref={endRef} />
        </div>

        {/* Quick replies */}
        {messages.length <= 1 && (
          <div className="px-4 pb-2">
            <div className="flex flex-wrap gap-1.5">
              {suggestions.map((s) => (
                <button
                  key={s}
                  onClick={() => send(s)}
                  className="rounded-full border border-neutral-100 bg-neutral-50 px-3 py-1.5 text-xs text-neutral-600 transition-colors hover:border-brand-300 hover:text-brand-700"
                >
                  {s}
                </button>
              ))}
            </div>
          </div>
        )}

        {/* Input */}
        <div className="px-4 pb-4 pt-2">
          <div className="flex items-center gap-2 rounded-xl border border-neutral-200 px-4 py-2.5 transition-colors focus-within:border-brand-500">
            <input
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={(e) => e.key === 'Enter' && send()}
              placeholder="Tell me what you are looking for..."
              className="flex-1 bg-transparent text-sm text-neutral-800 outline-none placeholder:text-neutral-400"
            />
            <button
              onClick={() => send()}
              disabled={!input.trim()}
              className="text-neutral-400 transition-colors hover:text-brand-600 disabled:opacity-30"
              aria-label="Send"
            >
              <Send size={16} />
            </button>
          </div>
        </div>
      </div>
    </>
  );
}
