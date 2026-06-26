import { useParams, Link } from 'react-router-dom';
import { useState } from 'react';
import { useCartStore, useWishlistStore } from '../store/cartStore';
import { products } from '../data/products';
import { Heart, ShoppingBag, ChevronLeft, Star, Check } from 'lucide-react';
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
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <p className="text-neutral-400 mb-4">Product not found.</p>
          <Link to="/shop" className="btn-primary">Back to Shop</Link>
        </div>
      </div>
    );
  }

  const handleAddToCart = () => {
    if (!selectedSize || !selectedColor) return;
    addItem(product, selectedSize, selectedColor);
    setAdded(true);
    setTimeout(() => setAdded(false), 2000);
  };

  const canAdd = selectedSize && selectedColor;

  return (
    <div className="min-h-screen pt-24 max-w-screen-xl mx-auto px-4 sm:px-6 py-8">
      <Link to="/shop" className="inline-flex items-center gap-1 text-sm text-neutral-500 hover:text-neutral-900 transition-colors mb-8">
        <ChevronLeft size={14} /> Back to Shop
      </Link>

      <div className="grid md:grid-cols-2 gap-10 lg:gap-16">
        {/* Images */}
        <div>
          <div className="aspect-[3/4] bg-neutral-100 overflow-hidden mb-4">
            <img
              src={product.images[selectedImg]}
              alt={product.name}
              className="w-full h-full object-cover"
            />
          </div>
          {product.images.length > 1 && (
            <div className="flex gap-2">
              {product.images.map((img, i) => (
                <button
                  key={i}
                  onClick={() => setSelectedImg(i)}
                  className={clsx(
                    'w-16 h-20 bg-neutral-100 overflow-hidden border-2 transition-colors',
                    selectedImg === i ? 'border-neutral-900' : 'border-transparent'
                  )}
                >
                  <img src={img} alt="" className="w-full h-full object-cover" />
                </button>
              ))}
            </div>
          )}
        </div>

        {/* Details */}
        <div className="flex flex-col">
          <p className="text-[10px] tracking-widest uppercase text-neutral-400 mb-1">{product.brand}</p>
          <h1 className="font-display text-2xl md:text-3xl font-semibold mb-2">{product.name}</h1>
          {product.nameEn && <p className="text-sm text-neutral-400 mb-4">{product.nameEn}</p>}

          {/* Rating */}
          <div className="flex items-center gap-2 mb-4">
            <div className="flex gap-0.5">
              {[...Array(5)].map((_, i) => (
                <Star
                  key={i}
                  size={14}
                  className={i < Math.floor(product.rating) ? 'fill-brand-500 text-brand-500' : 'text-neutral-200'}
                />
              ))}
            </div>
            <span className="text-xs text-neutral-400">({product.reviewCount} reviews)</span>
          </div>

          {/* Price */}
          <div className="flex items-center gap-3 mb-6">
            <span className="text-xl font-semibold text-neutral-900">${product.price.toLocaleString()}</span>
            {product.originalPrice && (
              <span className="text-base text-neutral-400 line-through">${product.originalPrice.toLocaleString()}</span>
            )}
          </div>

          {/* Quality Index (replaces sweetness) */}
          {product.material && (
            <div className="mb-4 p-3 bg-neutral-50 rounded-xl">
              <div className="flex items-center justify-between text-xs text-neutral-500 mb-1">
                <span>Quality Index</span>
                <span>{product.material}</span>
              </div>
              <div className="h-1.5 bg-neutral-200 rounded-full overflow-hidden">
                <div
                  className="h-full bg-brand-500 rounded-full"
                  style={{ width: `${Math.min(product.rating / 5 * 100, 100)}%` }}
                />
              </div>
            </div>
          )}

          {/* Color Selector */}
          <div className="mb-6">
            <p className="text-xs tracking-widest uppercase text-neutral-500 mb-3">Color: {selectedColor}</p>
            <div className="flex gap-2">
              {product.colors.map((c) => (
                <button
                  key={c.name}
                  onClick={() => setSelectedColor(c.name)}
                  className={clsx(
                    'w-8 h-8 rounded-full border-2 transition-all duration-150',
                    selectedColor === c.name ? 'border-neutral-900 scale-110' : 'border-neutral-200'
                  )}
                  style={{ background: c.hex }}
                  title={c.name}
                  aria-label={`Select color ${c.name}`}
                />
              ))}
            </div>
          </div>

          {/* Size Selector */}
          <div className="mb-6">
            <p className="text-xs tracking-widest uppercase text-neutral-500 mb-3">Size: {selectedSize}</p>
            <div className="flex gap-2 flex-wrap">
              {product.sizes.map((s) => (
                <button
                  key={s}
                  onClick={() => setSelectedSize(s)}
                  className={clsx(
                    'min-w-[3rem] px-3 py-2 border text-sm transition-all duration-150',
                    selectedSize === s
                      ? 'bg-neutral-900 text-white border-neutral-900'
                      : 'border-neutral-200 text-neutral-700 hover:border-neutral-900'
                  )}
                >
                  {s}
                </button>
              ))}
            </div>
          </div>

          {/* Specs Table */}
          {product.fit && (
            <div className="mb-6 text-sm">
              <div className="flex gap-6 py-2 border-b border-neutral-100">
                <span className="text-neutral-400 w-20">Fit</span>
                <span className="font-medium text-neutral-800">{product.fit}</span>
              </div>
              <div className="flex gap-6 py-2 border-b border-neutral-100">
                <span className="text-neutral-400 w-20">Material</span>
                <span className="font-medium text-neutral-800">{product.material}</span>
              </div>
            </div>
          )}

          {/* Description */}
          <p className="text-sm text-neutral-600 leading-relaxed mb-6">{product.description}</p>

          {/* Details List */}
          <ul className="mb-8 space-y-1">
            {product.details.map((d) => (
              <li key={d} className="text-sm text-neutral-600 flex items-start gap-2">
                <Check size={14} className="text-brand-500 mt-0.5 shrink-0" />
                {d}
              </li>
            ))}
          </ul>

          {/* Actions */}
          <div className="flex gap-3 mt-auto">
            <button
              onClick={handleAddToCart}
              disabled={!canAdd}
              className={clsx(
                'flex-1 btn-primary gap-2',
                (!canAdd || added) && 'opacity-60'
              )}
            >
              <ShoppingBag size={16} />
              {added ? 'Added!' : 'Add to Cart'}
            </button>
            <button
              onClick={() => toggle(product.id)}
              className={clsx(
                'p-3 border transition-all duration-200',
                wishlisted ? 'bg-neutral-900 border-neutral-900 text-white' : 'border-neutral-200 hover:border-neutral-900'
              )}
              aria-label={wishlisted ? 'Remove from wishlist' : 'Add to wishlist'}
            >
              <Heart size={18} className={wishlisted ? 'fill-white text-white' : ''} />
            </button>
          </div>

          {/* Trust Badges */}
          <div className="flex flex-wrap gap-4 mt-8 pt-6 border-t border-neutral-100 text-xs text-neutral-500">
            <span>Free shipping over $99</span>
            <span>30-day returns</span>
            <span>Secure checkout</span>
          </div>
        </div>
      </div>
    </div>
  );
}
