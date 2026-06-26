import { useState, useMemo } from 'react';
import { useSearchParams } from 'react-router-dom';
import { SlidersHorizontal, Grid, List, X, ChevronDown } from 'lucide-react';
import { products, categories } from '../data/products';
import ProductCard from '../components/ProductCard';
import { Category } from '../types';
import clsx from 'clsx';

const sortOptions = [
  { value: 'default', label: 'Default' },
  { value: 'price-asc', label: 'Price: Low to High' },
  { value: 'price-desc', label: 'Price: High to Low' },
  { value: 'rating', label: 'Highest Rated' },
  { value: 'newest', label: 'Newest First' },
];

export default function ShopPage() {
  const [searchParams, setSearchParams] = useSearchParams();
  const [layout, setLayout] = useState<'grid' | 'list'>('grid');
  const [filterOpen, setFilterOpen] = useState(false);
  const [sort, setSort] = useState('default');
  const [priceRange, setPriceRange] = useState<[number, number]>([0, 5000]);

  const activeCategory = (searchParams.get('category') || 'all') as string;
  const activeTag = searchParams.get('tag') || '';

  const setCategory = (cat: string) => {
    setSearchParams((prev) => {
      const p = new URLSearchParams(prev);
      p.set('category', cat);
      p.delete('tag');
      return p;
    });
  };

  const filtered = useMemo(() => {
    let list = [...products];
    if (activeCategory !== 'all') list = list.filter((p) => p.category === activeCategory);
    if (activeTag) list = list.filter((p) => p.tags.includes(activeTag));
    list = list.filter((p) => p.price >= priceRange[0] && p.price <= priceRange[1]);
    switch (sort) {
      case 'price-asc': return list.sort((a, b) => a.price - b.price);
      case 'price-desc': return list.sort((a, b) => b.price - a.price);
      case 'rating': return list.sort((a, b) => b.rating - a.rating);
      case 'newest': return list.sort((a, _b) => (a.isNew ? -1 : 1));
      default: return list;
    }
  }, [activeCategory, activeTag, sort, priceRange]);

  return (
    <div className="min-h-screen pt-20">
      {/* Header */}
      <div className="max-w-screen-xl mx-auto px-4 sm:px-6 py-10">
        <h1 className="font-display text-4xl mb-2">
          {activeTag
            ? activeTag
            : categories.find((c) => c.key === activeCategory)?.label || 'All Products'}
        </h1>
        <p className="text-neutral-400 text-sm">{filtered.length} product{filtered.length !== 1 ? 's' : ''}</p>
      </div>

      {/* Category Tabs */}
      <div className="border-t border-b border-neutral-100 sticky top-16 md:top-20 z-30 bg-white">
        <div className="max-w-screen-xl mx-auto px-4 sm:px-6">
          <div className="flex items-center gap-8 overflow-x-auto scrollbar-none py-3">
            {categories.map((cat) => (
              <button
                key={cat.key}
                onClick={() => setCategory(cat.key)}
                className={clsx(
                  'text-xs tracking-widest uppercase whitespace-nowrap pb-0.5 transition-all duration-150',
                  activeCategory === cat.key && !activeTag
                    ? 'text-neutral-900 border-b-2 border-neutral-900'
                    : 'text-neutral-400 hover:text-neutral-700'
                )}
              >
                {cat.label}
              </button>
            ))}
          </div>
        </div>
      </div>

      <div className="max-w-screen-xl mx-auto px-4 sm:px-6 py-6">
        {/* Toolbar */}
        <div className="flex items-center justify-between mb-6 gap-4">
          <button
            className="flex items-center gap-2 text-sm text-neutral-600 hover:text-neutral-900 transition-colors"
            onClick={() => setFilterOpen(!filterOpen)}
          >
            <SlidersHorizontal size={16} />
            Filters
            {filterOpen ? <X size={14} /> : <ChevronDown size={14} />}
          </button>

          <div className="flex items-center gap-4">
            {/* Sort */}
            <select
              value={sort}
              onChange={(e) => setSort(e.target.value)}
              className="text-sm border-0 text-neutral-600 bg-transparent cursor-pointer outline-none hover:text-neutral-900"
            >
              {sortOptions.map((o) => (
                <option key={o.value} value={o.value}>{o.label}</option>
              ))}
            </select>

            {/* Layout toggle */}
            <div className="hidden md:flex items-center gap-1 border border-neutral-200 p-1">
              <button
                className={clsx('p-1.5 transition-colors', layout === 'grid' ? 'bg-neutral-900 text-white' : 'text-neutral-400 hover:text-neutral-700')}
                onClick={() => setLayout('grid')}
                aria-label="Grid view"
              >
                <Grid size={14} />
              </button>
              <button
                className={clsx('p-1.5 transition-colors', layout === 'list' ? 'bg-neutral-900 text-white' : 'text-neutral-400 hover:text-neutral-700')}
                onClick={() => setLayout('list')}
                aria-label="List view"
              >
                <List size={14} />
              </button>
            </div>
          </div>
        </div>

        {/* Filter Panel */}
        {filterOpen && (
          <div className="mb-8 p-6 bg-neutral-50 border border-neutral-100">
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
              <div>
                <h4 className="text-xs tracking-widest uppercase text-neutral-500 mb-3">Tags</h4>
                <div className="flex flex-wrap gap-2">
                  {['New', 'Hot', 'Sale', 'Classic', 'Editor Pick'].map((tag) => (
                    <button
                      key={tag}
                      onClick={() => {
                        setSearchParams((prev) => {
                          const p = new URLSearchParams(prev);
                          activeTag === tag ? p.delete('tag') : p.set('tag', tag);
                          return p;
                        });
                      }}
                      className={clsx(
                        'px-3 py-1 text-xs border transition-colors',
                        activeTag === tag
                          ? 'bg-neutral-900 text-white border-neutral-900'
                          : 'border-neutral-200 text-neutral-600 hover:border-neutral-400'
                      )}
                    >
                      {tag}
                    </button>
                  ))}
                </div>
              </div>
              <div className="md:col-span-2">
                <h4 className="text-xs tracking-widest uppercase text-neutral-500 mb-3">
                  Price: ${priceRange[0]} — ${priceRange[1]}
                </h4>
                <input
                  type="range"
                  min={0}
                  max={5000}
                  step={100}
                  value={priceRange[1]}
                  onChange={(e) => setPriceRange([priceRange[0], Number(e.target.value)])}
                  className="w-full accent-neutral-900"
                />
              </div>
            </div>
          </div>
        )}

        {/* Products Grid */}
        {filtered.length === 0 ? (
          <div className="py-32 text-center text-neutral-400">
            <p className="text-lg mb-2">No products match your filters</p>
            <button onClick={() => { setCategory('all'); setSearchParams(new URLSearchParams()); }} className="text-sm underline hover:text-neutral-700">
              Clear all filters
            </button>
          </div>
        ) : (
          <div
            className={clsx(
              layout === 'grid'
                ? 'grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4 md:gap-6'
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
