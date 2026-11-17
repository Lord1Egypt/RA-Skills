import { useMemo, useState } from 'react';
import { useSearchParams } from 'react-router-dom';
import { ChevronDown, Grid, List, SlidersHorizontal, X } from 'lucide-react';
import ProductCard from '../components/ProductCard';
import { categories, products } from '../data/products';
import { formatPrice } from '../utils/format';
import clsx from 'clsx';

const sortOptions = [
  { value: 'default', label: 'Default' },
  { value: 'price-asc', label: 'Price: low to high' },
  { value: 'price-desc', label: 'Price: high to low' },
  { value: 'rating', label: 'Top rated' },
  { value: 'newest', label: 'Newest first' },
];

const FILTER_TAGS = ['New', 'Bestseller', 'Sale', 'Classic', 'Curated'];
const PRICE_MAX = 4000;

export default function ShopPage() {
  const [searchParams, setSearchParams] = useSearchParams();
  const [layout, setLayout] = useState<'grid' | 'list'>('grid');
  const [filterOpen, setFilterOpen] = useState(false);
  const [sort, setSort] = useState('default');
  const [priceMax, setPriceMax] = useState(PRICE_MAX);

  const activeCategory = searchParams.get('category') || 'all';
  const activeTag = searchParams.get('tag') || '';

  const setCategory = (key: string) => {
    setSearchParams((prev) => {
      const p = new URLSearchParams(prev);
      p.set('category', key);
      p.delete('tag');
      return p;
    });
  };

  const toggleTag = (tag: string) => {
    setSearchParams((prev) => {
      const p = new URLSearchParams(prev);
      if (activeTag === tag) {
        p.delete('tag');
      } else {
        p.set('tag', tag);
      }
      return p;
    });
  };

  const filtered = useMemo(() => {
    let list = [...products];
    if (activeCategory !== 'all') list = list.filter((p) => p.category === activeCategory);
    if (activeTag) list = list.filter((p) => p.tags.includes(activeTag));
    list = list.filter((p) => p.price <= priceMax);
    switch (sort) {
      case 'price-asc':
        return list.sort((a, b) => a.price - b.price);
      case 'price-desc':
        return list.sort((a, b) => b.price - a.price);
      case 'rating':
        return list.sort((a, b) => b.rating - a.rating);
      case 'newest':
        return list.sort((a, b) => Number(b.isNew) - Number(a.isNew));
      default:
        return list;
    }
  }, [activeCategory, activeTag, sort, priceMax]);

  const heading = activeTag
    ? `${activeTag} products`
    : categories.find((c) => c.key === activeCategory)?.label || 'All Products';

  return (
    <div className="min-h-screen pt-20">
      {/* Header */}
      <div className="mx-auto max-w-screen-xl px-4 py-10 sm:px-6">
        <h1 className="mb-2 font-display text-4xl">{heading}</h1>
        <p className="text-sm text-neutral-400">{filtered.length} products</p>
      </div>

      {/* Category tabs */}
      <div className="sticky top-16 z-30 border-y border-neutral-100 bg-white md:top-20">
        <div className="mx-auto max-w-screen-xl px-4 sm:px-6">
          <div className="scrollbar-none flex items-center gap-8 overflow-x-auto py-3">
            {categories.map((cat) => (
              <button
                key={cat.key}
                onClick={() => setCategory(cat.key)}
                className={clsx(
                  'flex items-center gap-1.5 whitespace-nowrap pb-0.5 text-xs uppercase tracking-widest transition-all duration-150',
                  activeCategory === cat.key && !activeTag
                    ? 'border-b-2 border-brand-600 text-brand-700'
                    : 'text-neutral-400 hover:text-neutral-700'
                )}
              >
                <cat.icon size={14} />
                {cat.label}
              </button>
            ))}
          </div>
        </div>
      </div>

      <div className="mx-auto max-w-screen-xl px-4 py-6 sm:px-6">
        {/* Toolbar */}
        <div className="mb-6 flex items-center justify-between gap-4">
          <button
            className="flex items-center gap-2 text-sm text-neutral-600 transition-colors hover:text-neutral-900"
            onClick={() => setFilterOpen(!filterOpen)}
          >
            <SlidersHorizontal size={16} />
            Filter
            {filterOpen ? <X size={14} /> : <ChevronDown size={14} />}
          </button>

          <div className="flex items-center gap-4">
            <select
              value={sort}
              onChange={(e) => setSort(e.target.value)}
              className="cursor-pointer border-0 bg-transparent text-sm text-neutral-600 outline-none hover:text-neutral-900"
              aria-label="Sort by"
            >
              {sortOptions.map((o) => (
                <option key={o.value} value={o.value}>
                  {o.label}
                </option>
              ))}
            </select>

            <div className="hidden items-center gap-1 rounded-full border border-neutral-200 p-1 md:flex">
              <button
                className={clsx(
                  'rounded-full p-1.5 transition-colors',
                  layout === 'grid' ? 'bg-brand-600 text-white' : 'text-neutral-400 hover:text-neutral-700'
                )}
                onClick={() => setLayout('grid')}
                aria-label="Grid view"
              >
                <Grid size={14} />
              </button>
              <button
                className={clsx(
                  'rounded-full p-1.5 transition-colors',
                  layout === 'list' ? 'bg-brand-600 text-white' : 'text-neutral-400 hover:text-neutral-700'
                )}
                onClick={() => setLayout('list')}
                aria-label="List view"
              >
                <List size={14} />
              </button>
            </div>
          </div>
        </div>

        {/* Filter panel */}
        {filterOpen && (
          <div className="mb-8 rounded-2xl border border-neutral-100 bg-neutral-50 p-6">
            <div className="grid grid-cols-1 gap-6 md:grid-cols-3">
              <div>
                <h4 className="mb-3 text-xs uppercase tracking-widest text-neutral-500">Tags</h4>
                <div className="flex flex-wrap gap-2">
                  {FILTER_TAGS.map((tag) => (
                    <button
                      key={tag}
                      onClick={() => toggleTag(tag)}
                      className={clsx(
                        'rounded-full border px-3 py-1 text-xs transition-colors',
                        activeTag === tag
                          ? 'border-brand-600 bg-brand-600 text-white'
                          : 'border-neutral-200 text-neutral-600 hover:border-brand-300'
                      )}
                    >
                      {tag}
                    </button>
                  ))}
                </div>
              </div>
              <div className="md:col-span-2">
                <h4 className="mb-3 text-xs uppercase tracking-widest text-neutral-500">
                  Max price: {formatPrice(priceMax)}
                </h4>
                <input
                  type="range"
                  min={200}
                  max={PRICE_MAX}
                  step={100}
                  value={priceMax}
                  onChange={(e) => setPriceMax(Number(e.target.value))}
                  className="w-full accent-brand-600"
                  aria-label="Maximum price"
                />
              </div>
            </div>
          </div>
        )}

        {/* Product grid */}
        {filtered.length === 0 ? (
          <div className="py-32 text-center text-neutral-400">
            <p className="mb-2 text-lg">No products match these filters</p>
            <button
              onClick={() => {
                setSearchParams(new URLSearchParams());
                setPriceMax(PRICE_MAX);
              }}
              className="text-sm underline hover:text-neutral-700"
            >
              Clear all filters
            </button>
          </div>
        ) : (
          <div
            className={clsx(
              layout === 'grid'
                ? 'grid grid-cols-2 gap-4 md:grid-cols-3 md:gap-6 lg:grid-cols-4'
                : 'flex flex-col gap-6'
            )}
          >
            {filtered.map((p) => (
              <ProductCard key={p.id} product={p} layout={layout} />
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
