import { Link } from 'react-router-dom';
import { Heart, ShoppingBag, Star } from 'lucide-react';
import { Product } from '../types';
import { useCartStore, useWishlistStore } from '../store/cartStore';
import clsx from 'clsx';

interface ProductCardProps {
  product: Product;
  layout?: 'grid' | 'list';
}

export default function ProductCard({ product, layout = 'grid' }: ProductCardProps) {
  const { addItem } = useCartStore();
  const { toggle, has } = useWishlistStore();
  const wishlisted = has(product.id);

  const handleAddToCart = (e: React.MouseEvent) => {
    e.preventDefault();
    addItem(product, product.sizes[0], product.colors[0].name);
  };

  return (
    <Link
      to={`/product/${product.id}`}
      className={clsx('group relative block', layout === 'list' && 'flex gap-6')}
    >
      {/* Image */}
      <div
        className={clsx(
          'relative overflow-hidden bg-neutral-100',
          layout === 'grid' ? 'aspect-[3/4] w-full' : 'aspect-[3/4] w-48 shrink-0'
        )}
      >
        <img
          src={product.images[0]}
          alt={product.name}
          className="w-full h-full object-cover transition-transform duration-700 group-hover:scale-105"
          loading="lazy"
        />
        {/* Hover second image */}
        {product.images[1] && (
          <img
            src={product.images[1]}
            alt={product.name}
            className="absolute inset-0 w-full h-full object-cover opacity-0 group-hover:opacity-100 transition-opacity duration-500"
          />
        )}

        {/* Badges */}
        <div className="absolute top-3 left-3 flex flex-col gap-1.5">
          {product.isNew && <span className="tag bg-neutral-900 text-white">NEW</span>}
          {product.isSale && <span className="tag bg-brand-500 text-white">SALE</span>}
        </div>

        {/* Wishlist */}
        <button
          className={clsx(
            'absolute top-3 right-3 p-2 bg-white rounded-full shadow-sm transition-all duration-200 opacity-0 group-hover:opacity-100 hover:scale-110',
            wishlisted && '!opacity-100'
          )}
          onClick={(e) => {
            e.preventDefault();
            toggle(product.id);
          }}
          aria-label={wishlisted ? 'Remove from wishlist' : 'Add to wishlist'}
        >
          <Heart
            size={15}
            className={clsx(wishlisted ? 'fill-neutral-900 text-neutral-900' : 'text-neutral-600')}
          />
        </button>

        {/* Quick Add */}
        <div className="absolute bottom-0 left-0 right-0 p-3 translate-y-full group-hover:translate-y-0 transition-transform duration-300">
          <button className="w-full btn-primary text-xs py-2.5 gap-1.5" onClick={handleAddToCart}>
            <ShoppingBag size={14} />
            Quick Add
          </button>
        </div>
      </div>

      {/* Info */}
      <div className={clsx('mt-3', layout === 'list' && 'flex-1 mt-0 flex flex-col justify-center')}>
        <p className="text-[10px] tracking-widest uppercase text-neutral-400 mb-1">{product.brand}</p>
        <h3 className="text-sm font-medium text-neutral-800 group-hover:text-neutral-600 transition-colors">
          {product.name}
        </h3>
        {product.nameEn && <p className="text-xs text-neutral-400 mb-2">{product.nameEn}</p>}

        {/* Rating */}
        <div className="flex items-center gap-1.5 mb-2">
          <div className="flex gap-0.5">
            {[...Array(5)].map((_, i) => (
              <Star
                key={i}
                size={11}
                className={
                  i < Math.floor(product.rating) ? 'fill-brand-500 text-brand-500' : 'text-neutral-200'
                }
              />
            ))}
          </div>
          <span className="text-[11px] text-neutral-400">({product.reviewCount})</span>
        </div>

        {/* Price */}
        <div className="flex items-center gap-2">
          <span className="text-sm font-semibold text-neutral-900">${product.price.toLocaleString()}</span>
          {product.originalPrice && (
            <span className="text-sm text-neutral-400 line-through">
              ${product.originalPrice.toLocaleString()}
            </span>
          )}
        </div>

        {/* Colors (list view only) */}
        {layout === 'list' && (
          <div className="flex gap-1.5 mt-3">
            {product.colors.map((c) => (
              <span
                key={c.name}
                className="w-5 h-5 rounded-full border border-neutral-200 cursor-pointer hover:ring-2 hover:ring-offset-1 hover:ring-neutral-400"
                style={{ background: c.hex }}
                title={c.name}
              />
            ))}
          </div>
        )}
      </div>
    </Link>
  );
}
