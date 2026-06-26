import { Link } from 'react-router-dom';
import { Heart, ShoppingBag } from 'lucide-react';
import { useCartStore, useWishlistStore } from '../store/cartStore';
import ProductCard from '../components/ProductCard';
import { products } from '../data/products';
import clsx from 'clsx';

export default function WishlistPage() {
  const { toggle, ids } = useWishlistStore();
  const { addItem } = useCartStore();

  const wishlistProducts = products.filter((p) => ids.includes(p.id));

  const handleAddAllToCart = () => {
    wishlistProducts.forEach((p) => {
      addItem(p, p.sizes[0], p.colors[0].name);
    });
  };

  return (
    <div className="min-h-screen pt-24 max-w-screen-xl mx-auto px-4 sm:px-6 py-10">
      <div className="flex items-end justify-between gap-4 mb-10 flex-wrap">
        <div>
          <h1 className="font-display text-3xl md:text-4xl font-semibold">Wishlist</h1>
          <p className="text-neutral-400 text-sm mt-1">
            {wishlistProducts.length} saved item{wishlistProducts.length !== 1 ? 's' : ''}
          </p>
        </div>
        {wishlistProducts.length > 0 && (
          <button onClick={handleAddAllToCart} className="btn-primary text-xs py-2.5 gap-2">
            <ShoppingBag size={14} />
            Add All to Cart
          </button>
        )}
      </div>

      {wishlistProducts.length === 0 ? (
        <div className="text-center py-32 text-neutral-400">
          <Heart size={48} strokeWidth={1} className="mx-auto mb-4" />
          <p className="text-lg mb-2">Your wishlist is empty</p>
          <p className="text-sm mb-6">Save items you love for later.</p>
          <Link to="/shop" className="btn-primary">
            Explore Products
          </Link>
        </div>
      ) : (
        <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4 md:gap-6">
          {wishlistProducts.map((p) => (
            <div key={p.id} className="relative group">
              <ProductCard product={p} layout="grid" />
              <button
                onClick={() => toggle(p.id)}
                className="absolute top-3 right-3 p-2 bg-white rounded-full shadow-sm hover:scale-110 transition-all duration-200 z-10"
                aria-label="Remove from wishlist"
              >
                <Heart size={15} className="fill-neutral-900 text-neutral-900" />
              </button>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
