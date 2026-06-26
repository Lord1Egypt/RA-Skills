import { useEffect, useState } from 'react';
import { motion } from 'framer-motion';
import { Link } from 'react-router-dom';
import { ArrowRight, Truck, Shield, RotateCcw, Sparkles } from 'lucide-react';
import { products, categories } from '../data/products';
import ProductCard from '../components/ProductCard';
import AIChatWidget from '../components/AIChatWidget';
import clsx from 'clsx';

const features = [
  {
    icon: Truck,
    title: 'Free Shipping',
    desc: 'On orders over $99. Express options available at checkout.',
  },
  {
    icon: Shield,
    title: 'Secure Payment',
    desc: 'SSL encrypted. We never store your card details.',
  },
  {
    icon: RotateCcw,
    title: 'Easy Returns',
    desc: '30-day no-questions-asked return policy.',
  },
  {
    icon: Sparkles,
    title: 'AI Assistant',
    desc: 'Get personalized recommendations from our AI concierge.',
  },
];

function HomePage() {
  const newArrivals = products.filter((p) => p.isNew).slice(0, 8);
  const bestsellers = [...products].sort((a, b) => b.reviewCount - a.reviewCount).slice(0, 4);

  return (
    <div className="min-h-screen">
      {/* Hero Section */}
      <section className="relative min-h-[80vh] flex items-center justify-center overflow-hidden bg-neutral-900 text-white">
        <div className="absolute inset-0 opacity-20">
          <img
            src={products[0]?.images[0]}
            alt=""
            className="w-full h-full object-cover"
          />
        </div>
        <div className="relative z-10 text-center px-4 max-w-3xl mx-auto">
          <motion.div
            initial={{ opacity: 0, y: 30 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8 }}
          >
            <span className="inline-block px-3 py-1 text-xs tracking-[0.2em] uppercase border border-white/30 rounded-full mb-6">
              New Collection Available
            </span>
            <h1 className="font-display text-4xl md:text-6xl lg:text-7xl font-bold tracking-tight leading-[0.95] mb-6">
              __SITE_NAME__<br />
              <span className="text-neutral-400">Collection</span>
            </h1>
            <p className="text-base md:text-lg text-neutral-300 max-w-xl mx-auto mb-8 leading-relaxed">
              Premium craftsmanship meets modern design. Discover pieces that define
              your personal style.
            </p>
            <div className="flex items-center justify-center gap-4 flex-wrap">
              <Link to="/shop" className="btn-primary">
                Shop Now
                <ArrowRight size={16} />
              </Link>
              <Link to="/shop?tag=Sale" className="btn-outline !border-white/40 !text-white hover:!bg-white hover:!text-neutral-900">
                View Sale
              </Link>
            </div>
          </motion.div>
        </div>
      </section>

      {/* Categories */}
      <section className="max-w-screen-xl mx-auto px-4 sm:px-6 py-16 md:py-24">
        <div className="text-center mb-12">
          <h2 className="section-title">Shop by Category</h2>
          <p className="section-subtitle">Find exactly what you are looking for</p>
        </div>
        <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-4">
          {categories
            .filter((c) => c.key !== 'all')
            .map((cat, i) => (
              <Link
                key={cat.key}
                to={`/shop?category=${cat.key}`}
                className="group relative aspect-square overflow-hidden bg-neutral-100"
              >
                <div className="absolute inset-0 bg-neutral-900/40 group-hover:bg-neutral-900/20 transition-colors duration-300 z-10 flex items-end p-4">
                  <span className="text-white font-medium tracking-wider uppercase text-sm">
                    {cat.label}
                  </span>
                </div>
                <div className="absolute inset-0 bg-neutral-200 animate-pulse group-hover:scale-105 transition-transform duration-700" />
              </Link>
            ))}
        </div>
      </section>

      {/* New Arrivals */}
      <section className="max-w-screen-xl mx-auto px-4 sm:px-6 py-16 md:py-24 border-t border-neutral-100">
        <div className="flex items-end justify-between gap-4 mb-10 flex-wrap">
          <div>
            <h2 className="section-title">New Arrivals</h2>
            <p className="section-subtitle">Fresh off the line — just for you</p>
          </div>
          <Link to="/shop?tag=New" className="btn-ghost gap-1">
            View All <ArrowRight size={14} />
          </Link>
        </div>
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4 md:gap-6">
          {newArrivals.map((p) => (
            <ProductCard key={p.id} product={p} />
          ))}
        </div>
      </section>

      {/* Features */}
      <section className="bg-neutral-50 py-16 md:py-24">
        <div className="max-w-screen-xl mx-auto px-4 sm:px-6">
          <div className="grid grid-cols-2 md:grid-cols-4 gap-8">
            {features.map((f) => (
              <div key={f.title} className="text-center">
                <div className="inline-flex items-center justify-center w-12 h-12 bg-white rounded-full shadow-sm mb-4">
                  <f.icon size={20} className="text-neutral-700" />
                </div>
                <h3 className="text-sm font-semibold text-neutral-800 mb-1">{f.title}</h3>
                <p className="text-xs text-neutral-500 leading-relaxed">{f.desc}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Bestsellers */}
      <section className="max-w-screen-xl mx-auto px-4 sm:px-6 py-16 md:py-24">
        <div className="flex items-end justify-between gap-4 mb-10 flex-wrap">
          <div>
            <h2 className="section-title">Bestsellers</h2>
            <p className="section-subtitle">Loved by our community</p>
          </div>
        </div>
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4 md:gap-6">
          {bestsellers.map((p) => (
            <ProductCard key={p.id} product={p} />
          ))}
        </div>
      </section>

      {/* Brand Story */}
      <section className="bg-neutral-900 text-white py-16 md:py-24">
        <div className="max-w-screen-xl mx-auto px-4 sm:px-6 grid md:grid-cols-2 gap-12 items-center">
          <div className="aspect-[4/3] bg-neutral-800 overflow-hidden">
            <div className="w-full h-full bg-neutral-700 animate-pulse" />
          </div>
          <div>
            <span className="text-xs tracking-[0.2em] uppercase text-neutral-400 mb-3 block">
              Our Story
            </span>
            <h2 className="font-display text-3xl md:text-4xl font-bold mb-6">
              Crafted with Passion
            </h2>
            <p className="text-neutral-300 leading-relaxed mb-6">
              __BRAND_NAME__ was founded with a simple mission: create premium products
              that blend timeless design with modern comfort. Every piece is carefully
              crafted using the finest materials, ensuring both style and durability.
            </p>
            <p className="text-neutral-400 leading-relaxed mb-8 text-sm">
              From our studio to your wardrobe — we believe good design should be
              accessible, comfortable, and made to last.
            </p>
            <Link
              to="/shop"
              className="inline-flex items-center gap-2 text-sm font-medium text-white border-b border-white/30 pb-1 hover:border-white transition-colors"
            >
              Discover Our Collection <ArrowRight size={14} />
            </Link>
          </div>
        </div>
      </section>

      {/* AI Assistant CTA */}
      <section className="max-w-screen-xl mx-auto px-4 sm:px-6 py-16 md:py-24 text-center">
        <Sparkles size={32} className="text-brand-500 mx-auto mb-4" />
        <h2 className="font-display text-2xl md:text-3xl font-bold mb-3">
          Not sure where to start?
        </h2>
        <p className="text-neutral-500 mb-6 max-w-md mx-auto">
          Our AI assistant can help you find the perfect pieces based on your style,
          fit, and budget.
        </p>
        <span className="text-sm text-neutral-400">
          Scroll down and click the sparkle button in the bottom-right corner
        </span>
      </section>

      <AIChatWidget />
    </div>
  );
}

export default HomePage;
