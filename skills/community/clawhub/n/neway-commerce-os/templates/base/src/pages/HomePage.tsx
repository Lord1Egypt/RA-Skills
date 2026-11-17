import { Link } from 'react-router-dom';
import { motion } from 'framer-motion';
import { ArrowRight, ShieldCheck, Sparkles, Truck } from 'lucide-react';
import { categories, products } from '../data/products';
import ProductCard from '../components/ProductCard';

const fadeUp = {
  hidden: { opacity: 0, y: 20 },
  visible: { opacity: 1, y: 0 },
};

const stagger = {
  hidden: {},
  visible: { transition: { staggerChildren: 0.08 } },
};

function HomePage() {
  const newArrivals = products.filter((p) => p.isNew).slice(0, 8);
  const bestsellers = [...products]
    .filter((p) => p.rating >= 4.7)
    .sort((a, b) => b.reviewCount - a.reviewCount)
    .slice(0, 4);
  const heroImage = products[0]?.images[0];
  const storyImage = '/images/1598300042247.jpg';

  return (
    <div className="min-h-screen">
      {/* Hero */}
      <section className="relative flex min-h-[80vh] items-center justify-center overflow-hidden bg-neutral-900 text-white">
        <div className="absolute inset-0 opacity-25">
          {heroImage && <img src={heroImage} alt="" className="h-full w-full object-cover" />}
        </div>
        <div className="relative z-10 mx-auto max-w-3xl px-4 text-center">
          <motion.div initial={{ opacity: 0, y: 30 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.8 }}>
            <span className="mb-6 inline-block rounded-full border border-white/30 px-3 py-1 text-xs uppercase tracking-[0.2em]">
              New season, now in stock
            </span>
            <h1 className="mb-6 font-display text-4xl font-bold leading-[1.05] tracking-tight md:text-6xl">
              __SITE_NAME__
              <br />
              <span className="text-neutral-400">The new season</span>
            </h1>
            <p className="mx-auto mb-8 max-w-xl text-base leading-relaxed text-neutral-300 md:text-lg">
              We design by taking things away, not adding them. Everything here is made to be worn again,
              not replaced.
            </p>
            <div className="flex flex-wrap items-center justify-center gap-4">
              <Link to="/shop" className="btn-primary">
                Shop now
                <ArrowRight size={16} />
              </Link>
              <Link
                to="/shop?tag=Sale"
                className="btn-outline border-white/40 text-white hover:bg-white hover:text-neutral-900"
              >
                View sale
              </Link>
            </div>
          </motion.div>
        </div>
      </section>

      {/* Category banners */}
      <section className="mx-auto max-w-screen-xl px-4 py-16 sm:px-6 md:py-24">
        <div className="mb-12 text-center">
          <h2 className="section-title">Shop by category</h2>
          <p className="section-subtitle">Six categories that cover a whole week of dressing</p>
        </div>
        <motion.div
          variants={stagger}
          initial="hidden"
          whileInView="visible"
          viewport={{ once: true }}
          className="grid grid-cols-2 gap-4 md:grid-cols-3 lg:grid-cols-6"
        >
          {categories
            .filter((c) => c.key !== 'all')
            .map((cat) => (
              <motion.div key={cat.key} variants={fadeUp}>
                <Link
                  to={`/shop?category=${cat.key}`}
                  className="group relative block aspect-square overflow-hidden rounded-xl bg-neutral-100"
                >
                  <img
                    src={cat.image}
                    alt={cat.label}
                    className="h-full w-full object-cover transition-transform duration-700 group-hover:scale-110"
                    loading="lazy"
                  />
                  <div className="absolute inset-0 flex items-end bg-neutral-900/45 p-4 transition-colors duration-300 group-hover:bg-brand-600/60">
                    <span className="flex items-center gap-1.5 text-sm font-medium uppercase tracking-wider text-white">
                      <cat.icon size={16} />
                      {cat.label}
                    </span>
                  </div>
                </Link>
              </motion.div>
            ))}
        </motion.div>
      </section>

      {/* New arrivals */}
      <section className="mx-auto max-w-screen-xl border-t border-neutral-100 px-4 py-16 sm:px-6 md:py-24">
        <div className="mb-10 flex flex-wrap items-end justify-between gap-4">
          <div>
            <h2 className="section-title">New arrivals</h2>
            <p className="section-subtitle">Fresh in this season, with a full size run</p>
          </div>
          <Link to="/shop?tag=New" className="btn-ghost">
            View all
            <ArrowRight size={14} />
          </Link>
        </div>
        <motion.div
          variants={stagger}
          initial="hidden"
          whileInView="visible"
          viewport={{ once: true }}
          className="grid grid-cols-2 gap-4 md:grid-cols-4 md:gap-6"
        >
          {newArrivals.map((p) => (
            <motion.div key={p.id} variants={fadeUp}>
              <ProductCard product={p} />
            </motion.div>
          ))}
        </motion.div>
      </section>

      {/* Bestsellers */}
      <section className="mx-auto max-w-screen-xl px-4 py-16 sm:px-6 md:py-24">
        <div className="mb-10 flex flex-wrap items-end justify-between gap-4">
          <div>
            <h2 className="section-title">Bestsellers</h2>
            <p className="section-subtitle">Rated 4.7 and up, and the most repurchased</p>
          </div>
        </div>
        <motion.div
          variants={stagger}
          initial="hidden"
          whileInView="visible"
          viewport={{ once: true }}
          className="grid grid-cols-2 gap-4 md:grid-cols-4 md:gap-6"
        >
          {bestsellers.map((p) => (
            <motion.div key={p.id} variants={fadeUp}>
              <ProductCard product={p} />
            </motion.div>
          ))}
        </motion.div>
      </section>

      {/* Brand story */}
      <section className="bg-neutral-900 py-16 text-white md:py-24">
        <div className="mx-auto grid max-w-screen-xl items-center gap-12 px-4 sm:px-6 md:grid-cols-2">
          <div className="aspect-[4/3] overflow-hidden rounded-2xl bg-neutral-800">
            <img src={storyImage} alt="" className="h-full w-full object-cover" loading="lazy" />
          </div>
          <div>
            <span className="mb-3 block text-xs uppercase tracking-[0.2em] text-neutral-400">Our story</span>
            <h2 className="mb-6 font-display text-3xl font-bold md:text-4xl">Spend the budget on fabric</h2>
            <p className="mb-6 leading-relaxed text-neutral-300">
              __BRAND_NAME__ started in a studio with three sewing machines. We do not work at the pace of
              fast fashion — we make clothes you can still wear in three years. Fabric passes first;
              then we talk about the cut.
            </p>
            <p className="mb-8 text-sm leading-relaxed text-neutral-400">
              Every garment lists its real composition and where it was made, with no vague wording.
              That is the floor, not the promise.
            </p>
            <Link
              to="/shop"
              className="inline-flex items-center gap-2 border-b border-white/30 pb-1 text-sm font-medium text-white transition-colors hover:border-white"
            >
              Browse everything
              <ArrowRight size={14} />
            </Link>
          </div>
        </div>
      </section>

      {/* AI assistant entry */}
      <section className="mx-auto max-w-screen-xl px-4 py-16 text-center sm:px-6 md:py-24">
        <Sparkles size={32} className="mx-auto mb-4 text-brand-500" />
        <h2 className="mb-3 font-display text-2xl font-bold md:text-3xl">Not sure where to start?</h2>
        <p className="mx-auto mb-6 max-w-md text-neutral-500">
          The assistant in the bottom right corner narrows things down by occasion, budget and style,
          and hands you pieces you can add to the cart straight away.
        </p>
        <div className="mx-auto flex max-w-md flex-wrap items-center justify-center gap-6 text-xs text-neutral-500">
          <span className="flex items-center gap-1.5">
            <Truck size={14} />
            Free shipping over ¥299
          </span>
          <span className="flex items-center gap-1.5">
            <ShieldCheck size={14} />
            30-day returns
          </span>
        </div>
      </section>
    </div>
  );
}

export default HomePage;
