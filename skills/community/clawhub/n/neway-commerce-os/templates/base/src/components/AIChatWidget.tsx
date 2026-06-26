import { useState, useRef, useEffect } from 'react';
import { X, Send, Sparkles, ShoppingBag } from 'lucide-react';
import { Link } from 'react-router-dom';
import { products } from '../data/products';
import { Product } from '../types';
import clsx from 'clsx';

interface Message {
  role: 'user' | 'assistant';
  content: string;
  products?: Product[];
}

const suggestions = [
  'Recommend something for everyday wear',
  'Show me the latest arrivals',
  'What are your bestsellers?',
  'I need a gift idea, budget $100',
];

function mockAIResponse(input: string): { content: string; products: Product[] } {
  const lower = input.toLowerCase();

  if (lower.includes('gift') || lower.includes('present')) {
    const recs = [...products].sort((a, b) => b.rating - a.rating).slice(0, 3);
    const match = input.match(/(\d+)/);
    const budget = match ? parseInt(match[1]) : null;
    const filtered = budget ? recs.filter((p) => p.price <= budget) : recs;
    return {
      content: `Great choice! Here are our top-rated picks${budget ? ` within $${budget}` : ''}. Each one makes a thoughtful gift with premium quality and presentation.`,
      products: filtered.length > 0 ? filtered : recs,
    };
  }

  if (lower.includes('new') || lower.includes('latest') || lower.includes('arrival')) {
    const recs = products.filter((p) => p.isNew);
    return {
      content: `Here's what just dropped. Fresh styles, premium materials — check out our latest collection:`,
      products: recs,
    };
  }

  if (lower.includes('sale') || lower.includes('discount') || lower.includes('deal')) {
    const recs = products.filter((p) => p.isSale);
    return {
      content: `Don't miss these deals! Premium quality at great prices while stocks last:`,
      products: recs,
    };
  }

  if (lower.includes('best') || lower.includes('popular') || lower.includes('top')) {
    const recs = [...products].sort((a, b) => b.reviewCount - a.reviewCount).slice(0, 4);
    return {
      content: 'Our community favorites — tried, tested, and loved by many:',
      products: recs,
    };
  }

  if (lower.includes('budget') || lower.includes('price') || lower.includes('affordable')) {
    const match = input.match(/(\d+)/);
    const budget = match ? parseInt(match[1]) : 500;
    const recs = products
      .filter((p) => p.price <= budget)
      .sort((a, b) => b.rating - a.rating)
      .slice(0, 4);
    return {
      content: `Here are our highest-rated items at $${budget} or under. Great quality, smart value:`,
      products: recs,
    };
  }

  if (lower.includes('premium') || lower.includes('luxury') || lower.includes('exclusive')) {
    const recs = [...products].sort((a, b) => b.price - a.price).slice(0, 3);
    return {
      content: 'For those who appreciate the finest. Our most exclusive pieces, crafted with the best materials:',
      products: recs,
    };
  }

  // Default: recommend top-rated
  const recs = [...products].sort((a, b) => b.rating - a.rating).slice(0, 3);
  return {
    content:
      "Hi! I'm your AI shopping assistant at __BRAND_NAME__. Tell me what you're looking for — style, occasion, budget — and I'll find the perfect match.",
    products: recs,
  };
}

export default function AIChatWidget() {
  const [open, setOpen] = useState(false);
  const [messages, setMessages] = useState<Message[]>([
    {
      role: 'assistant',
      content:
        "Hi! I'm your AI shopping assistant at __BRAND_NAME__. Tell me what you're looking for and I'll help you find the perfect piece.",
    },
  ]);
  const [input, setInput] = useState('');
  const [typing, setTyping] = useState(false);
  const endRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    endRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages, typing]);

  const send = async (text?: string) => {
    const msg = text || input.trim();
    if (!msg) return;
    setInput('');

    setMessages((m) => [...m, { role: 'user', content: msg }]);
    setTyping(true);

    await new Promise((r) => setTimeout(r, 900 + Math.random() * 600));

    const { content, products: recs } = mockAIResponse(msg);
    setMessages((m) => [...m, { role: 'assistant', content, products: recs }]);
    setTyping(false);
  };

  return (
    <>
      {/* Float Button */}
      <button
        onClick={() => setOpen(true)}
        className={clsx(
          'fixed bottom-6 right-6 z-40 w-14 h-14 bg-neutral-900 text-white rounded-full shadow-2xl flex items-center justify-center hover:bg-neutral-700 transition-all duration-200 hover:scale-110',
          open && 'hidden'
        )}
        aria-label="Open AI assistant"
      >
        <Sparkles size={22} />
      </button>

      {/* Chat Window */}
      <div
        className={clsx(
          'fixed bottom-6 right-6 z-40 w-96 max-h-[600px] bg-white shadow-2xl rounded-2xl flex flex-col transition-all duration-300 origin-bottom-right',
          open ? 'opacity-100 scale-100 pointer-events-auto' : 'opacity-0 scale-90 pointer-events-none'
        )}
      >
        {/* Header */}
        <div className="flex items-center justify-between px-5 py-4 bg-neutral-900 rounded-t-2xl">
          <div className="flex items-center gap-2">
            <Sparkles size={16} className="text-brand-300" />
            <span className="font-medium text-white text-sm">AI Assistant</span>
          </div>
          <button
            onClick={() => setOpen(false)}
            className="text-white/60 hover:text-white transition-colors"
            aria-label="Close assistant"
          >
            <X size={18} />
          </button>
        </div>

        {/* Messages */}
        <div className="flex-1 overflow-y-auto p-4 space-y-4 min-h-0">
          {messages.map((m, i) => (
            <div key={i} className={clsx('flex', m.role === 'user' ? 'justify-end' : 'justify-start')}>
              <div
                className={clsx(
                  'max-w-[85%] rounded-2xl px-4 py-3 text-sm leading-relaxed',
                  m.role === 'user'
                    ? 'bg-neutral-900 text-white rounded-br-sm'
                    : 'bg-neutral-50 text-neutral-800 rounded-bl-sm'
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
                        className="flex items-center gap-3 p-2 bg-white rounded-xl border border-neutral-100 hover:border-neutral-300 transition-colors"
                      >
                        <img
                          src={p.images[0]}
                          alt={p.name}
                          className="w-12 h-14 object-cover rounded-lg bg-neutral-100"
                        />
                        <div className="flex-1 min-w-0">
                          <p className="text-xs font-medium text-neutral-800 truncate">{p.name}</p>
                          {p.nameEn && <p className="text-xs text-neutral-400 truncate">{p.nameEn}</p>}
                          <div className="flex items-center gap-1 mt-1">
                            <span className="text-xs font-semibold text-neutral-900">
                              ${p.price.toLocaleString()}
                            </span>
                            {p.isNew && (
                              <span className="text-[10px] bg-neutral-900 text-white px-1.5 py-0.5 rounded">
                                NEW
                              </span>
                            )}
                          </div>
                        </div>
                        <ShoppingBag size={14} className="text-neutral-400 shrink-0" />
                      </Link>
                    ))}
                  </div>
                )}
              </div>
            </div>
          ))}
          {typing && (
            <div className="flex justify-start">
              <div className="bg-neutral-50 rounded-2xl rounded-bl-sm px-4 py-3">
                <div className="flex gap-1">
                  <span
                    className="w-2 h-2 bg-neutral-400 rounded-full animate-bounce"
                    style={{ animationDelay: '0ms' }}
                  />
                  <span
                    className="w-2 h-2 bg-neutral-400 rounded-full animate-bounce"
                    style={{ animationDelay: '150ms' }}
                  />
                  <span
                    className="w-2 h-2 bg-neutral-400 rounded-full animate-bounce"
                    style={{ animationDelay: '300ms' }}
                  />
                </div>
              </div>
            </div>
          )}
          <div ref={endRef} />
        </div>

        {/* Suggestions */}
        {messages.length <= 1 && (
          <div className="px-4 pb-2">
            <div className="flex flex-wrap gap-1.5">
              {suggestions.map((s) => (
                <button
                  key={s}
                  onClick={() => send(s)}
                  className="text-xs px-3 py-1.5 bg-neutral-50 border border-neutral-100 text-neutral-600 rounded-full hover:border-neutral-300 hover:text-neutral-800 transition-colors"
                >
                  {s}
                </button>
              ))}
            </div>
          </div>
        )}

        {/* Input */}
        <div className="px-4 pb-4 pt-2">
          <div className="flex items-center gap-2 border border-neutral-200 rounded-xl px-4 py-2.5 focus-within:border-neutral-400 transition-colors">
            <input
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={(e) => e.key === 'Enter' && send()}
              placeholder="Describe what you're looking for..."
              className="flex-1 text-sm outline-none bg-transparent text-neutral-800 placeholder-neutral-400"
            />
            <button
              onClick={() => send()}
              disabled={!input.trim()}
              className="text-neutral-400 hover:text-neutral-900 transition-colors disabled:opacity-30"
              aria-label="Send message"
            >
              <Send size={16} />
            </button>
          </div>
        </div>
      </div>
    </>
  );
}
