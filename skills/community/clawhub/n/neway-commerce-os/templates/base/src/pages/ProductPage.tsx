import { useState } from 'react';
import { Link, useParams } from 'react-router-dom';
import { Check, ChevronLeft, Heart, ShoppingBag, Star, Truck } from 'lucide-react';
import ProductCard from '../components/ProductCard';
import { products } from '../data/products';
import { useCartStore, useWishlistStore } from '../store/cartStore';
import { FREE_SHIPPING_THRESHOLD, formatPrice } from '../utils/format';
import clsx from 'clsx';

export default function ProductPage() {
  const { id } = useParams<{ id: string }>();
  const product = products.find((p) => p.id === id);
  const [selectedImg, setSelectedImg] = useState(0);
  const [selectedSize, setSelectedSize] = useState('');
  const [selectedColor, setSelectedColor] = useState('');
  const [added, setAdded] = useState(false);
  const { addItem } = useCartStore();
  const { toggle, has } = useWishlistStore();
  const wishlisted = product ? has(product.id) : false;

  if (!product) {
    return (
      <div className="flex min-h-screen items-center justify-center">
        <div className="text-center">
          <p className="mb-4 text-neutral-400">We could not find that product</p>
          <Link to="/shop" className="btn-primary">
            Back to shop
          </Link>
        </div>
      </div>
    );
  }

  const related = products
    .filter((p) => p.category === product.category && p.id !== product.id)
    .slice(0, 4);

  const canAdd = Boolean(selectedSize && selectedColor);

  const handleAddToCart = () => {
    if (!canAdd) return;
    addItem(product, selectedSize, selectedColor);
    setAdded(true);
    setTimeout(() => setAdded(false), 2000);
  };

  return (
    <div className="min-h-screen pt-24">
      <div className="mx-auto max-w-screen-xl px-4 py-8 sm:px-6">
        <Link
          to="/shop"
          className="mb-8 inline-flex items-center gap-1 text-sm text-neutral-500 transition-colors hover:text-brand-600"
        >
          <ChevronLeft size={14} />
          Back to shop
        </Link>

        <div className="grid gap-10 md:grid-cols-2 lg:gap-16">
          {/* Gallery */}
          <div>
            <div className="mb-4 aspect-[4/5] overflow-hidden rounded-2xl bg-neutral-100">
              <img src={product.images[selectedImg]} alt={product.name} className="h-full w-full object-cover" />
            </div>
            {product.images.length > 1 && (
              <div className="flex gap-2">
                {product.images.map((img, i) => (
                  <button
                    key={img}
                    onClick={() => setSelectedImg(i)}
                    className={clsx(
                      'h-20 w-16 overflow-hidden rounded-lg border-2 bg-neutral-100 transition-colors',
                      selectedImg === i ? 'border-brand-600' : 'border-transparent'
                    )}
                    aria-label={`View image ${i + 1}`}
                  >
                    <img src={img} alt="" className="h-full w-full object-cover" />
                  </button>
                ))}
              </div>
            )}
          </div>

          {/* Info */}
          <div className="flex flex-col">
            {/* Badges */}
            <div className="mb-3 flex flex-wrap items-center gap-2">
              {product.isNew && <span className="tag bg-brand-600 text-white">New</span>}
              {product.isSale && <span className="tag bg-fresh-600 text-white">Sale</span>}
              {product.stock <= 10 && (
                <span className="tag bg-neutral-900 text-white">Only {product.stock} left</span>
              )}
            </div>

            <p className="mb-1 text-[12px] uppercase tracking-widest text-neutral-400">{product.brand}</p>
            <h1 className="mb-1 font-display text-2xl font-semibold md:text-3xl">{product.name}</h1>
            {product.nameEn && <p className="mb-4 text-sm text-neutral-400">{product.nameEn}</p>}

            <p className="mb-6 text-sm text-neutral-600">{product.highlight}</p>

            {/* Rating + quality bar */}
            <div className="mb-6 flex items-center gap-3">
              <div className="flex gap-0.5" aria-hidden="true">
                {[1, 2, 3, 4, 5].map((level) => (
                  <span
                    key={level}
                    className={clsx(
                      'h-1.5 w-6 rounded-full',
                      level <= Math.round(product.rating) ? 'bg-brand-500' : 'bg-neutral-200'
                    )}
                  />
                ))}
              </div>
              <span className="flex items-center gap-1 text-xs text-neutral-500">
                <Star size={12} className="fill-brand-500 text-brand-500" />
                {product.rating.toFixed(1)} · {product.reviewCount} reviews
              </span>
            </div>

            {/* Price */}
            <div className="mb-6 flex items-baseline gap-3">
              <span className="text-2xl font-semibold text-neutral-900">{formatPrice(product.price)}</span>
              {product.originalPrice && (
                <span className="text-base text-neutral-400 line-through">
                  {formatPrice(product.originalPrice)}
                </span>
              )}
            </div>

            {/* Colors */}
            <div className="mb-6">
              <p className="mb-3 text-xs uppercase tracking-widest text-neutral-500">
                Colour: {selectedColor || 'Select one'}
              </p>
              <div className="flex gap-2">
                {product.colors.map((c) => (
                  <button
                    key={c.name}
                    onClick={() => setSelectedColor(c.name)}
                    className={clsx(
                      'h-8 w-8 rounded-full border-2 transition-all duration-150',
                      selectedColor === c.name ? 'scale-110 border-brand-600' : 'border-neutral-200'
                    )}
                    style={{ background: c.hex }}
                    title={c.name}
                    aria-label={`Select colour ${c.name}`}
                  />
                ))}
              </div>
            </div>

            {/* Sizes */}
            <div className="mb-6">
              <p className="mb-3 text-xs uppercase tracking-widest text-neutral-500">
                Size: {selectedSize || 'Select one'}
              </p>
              <div className="flex flex-wrap gap-2">
                {product.sizes.map((s) => (
                  <button
                    key={s}
                    onClick={() => setSelectedSize(s)}
                    className={clsx(
                      'min-w-[3rem] rounded-full border px-3 py-2 text-sm transition-all duration-150',
                      selectedSize === s
                        ? 'border-brand-600 bg-brand-600 text-white'
                        : 'border-neutral-200 text-neutral-700 hover:border-brand-600'
                    )}
                  >
                    {s}
                  </button>
                ))}
              </div>
            </div>

            {/* Specs */}
            <div className="mb-6 text-sm">
              <div className="flex gap-6 border-b border-neutral-100 py-2">
                <span className="w-20 text-neutral-400">Fit</span>
                <span className="font-medium text-neutral-800">{product.fit}</span>
              </div>
              <div className="flex gap-6 border-b border-neutral-100 py-2">
                <span className="w-20 text-neutral-400">Fabric</span>
                <span className="font-medium text-neutral-800">{product.material}</span>
              </div>
            </div>

            {/* Description */}
            <p className="mb-6 text-sm leading-relaxed text-neutral-600">{product.description}</p>

            {/* Details */}
            <ul className="mb-8 space-y-1">
              {product.details.map((d) => (
                <li key={d} className="flex items-start gap-2 text-sm text-neutral-600">
                  <Check size={14} className="mt-0.5 shrink-0 text-brand-500" />
                  {d}
                </li>
              ))}
            </ul>

            {/* Actions */}
            <div className="mt-auto flex gap-3">
              <button
                onClick={handleAddToCart}
                disabled={!canAdd}
                className={clsx('btn-primary flex-1', (!canAdd || added) && 'opacity-60')}
              >
                <ShoppingBag size={16} />
                {added ? 'Added to cart' : 'Add to cart'}
              </button>
              <button
                onClick={() => toggle(product.id)}
                className={clsx(
                  'rounded-full border p-3 transition-all duration-200',
                  wishlisted
                    ? 'border-brand-600 bg-brand-600 text-white'
                    : 'border-neutral-200 hover:border-brand-600'
                )}
                aria-label={wishlisted ? 'Remove from wishlist' : 'Add to wishlist'}
              >
                <Heart size={18} className={wishlisted ? 'fill-white' : ''} />
              </button>
            </div>

            {/* Delivery info */}
            <div className="mt-8 space-y-2 border-t border-neutral-100 pt-6 text-xs text-neutral-500">
              <p className="flex items-center gap-1.5">
                <Truck size={14} />
                Free shipping over {formatPrice(FREE_SHIPPING_THRESHOLD)} — arrives in 1–3 days
              </p>
              <p>30-day returns · invoices available</p>
              <p>Secure payment · encrypted end to end</p>
            </div>
          </div>
        </div>

        {/* Related products */}
        {related.length > 0 && (
          <section className="mt-20 border-t border-neutral-100 pt-12">
            <h2 className="section-title mb-8">You may also like</h2>
            <div className="grid grid-cols-2 gap-4 md:grid-cols-4 md:gap-6">
              {related.map((p) => (
                <ProductCard key={p.id} product={p} />
              ))}
            </div>
          </section>
        )}
      </div>
    </div>
  );
}
