import { Link } from 'react-router-dom';
import { Heart, ShoppingBag } from 'lucide-react';
import ProductCard from '../components/ProductCard';
import { products } from '../data/products';
import { useCartStore, useWishlistStore } from '../store/cartStore';

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
    <div className="mx-auto min-h-screen max-w-screen-xl px-4 py-10 pt-24 sm:px-6">
      <div className="mb-10 flex flex-wrap items-end justify-between gap-4">
        <div>
          <h1 className="font-display text-3xl font-semibold md:text-4xl">Wishlist</h1>
          <p className="mt-1 text-sm text-neutral-400">{wishlistProducts.length} saved</p>
        </div>
        {wishlistProducts.length > 0 && (
          <button onClick={handleAddAllToCart} className="btn-primary py-2.5 text-xs">
            <ShoppingBag size={14} />
            Add all to cart
          </button>
        )}
      </div>

      {wishlistProducts.length === 0 ? (
        <div className="py-32 text-center text-neutral-400">
          <Heart size={48} strokeWidth={1} className="mx-auto mb-4" />
          <p className="mb-2 text-lg">Your wishlist is empty</p>
          <p className="mb-6 text-sm">Save the pieces you like and come back to order them together.</p>
          <Link to="/shop" className="btn-primary">
            Browse products
          </Link>
        </div>
      ) : (
        <div className="grid grid-cols-2 gap-4 md:grid-cols-3 md:gap-6 lg:grid-cols-4">
          {wishlistProducts.map((p) => (
            <div key={p.id} className="group relative">
              <ProductCard product={p} />
              <button
                onClick={() => toggle(p.id)}
                className="absolute right-3 top-3 z-10 rounded-full bg-white p-2 shadow-sm transition-all duration-200 hover:scale-110"
                aria-label="Remove from wishlist"
              >
                <Heart size={16} className="fill-brand-600 text-brand-600" />
              </button>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
