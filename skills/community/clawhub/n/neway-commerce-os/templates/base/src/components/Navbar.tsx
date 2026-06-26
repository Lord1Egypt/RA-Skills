import { useState, useEffect } from 'react';
import { Link, useLocation } from 'react-router-dom';
import { ShoppingBag, Heart, Search, Menu, X } from 'lucide-react';
import { useCartStore } from '../store/cartStore';
import clsx from 'clsx';

const defaultNavLinks = [
  { label: 'New In', path: '/shop?tag=New' },
  { label: 'Category A', path: '/shop?category=category-a' },
  { label: 'Category B', path: '/shop?category=category-b' },
  { label: 'Category C', path: '/shop?category=category-c' },
  { label: 'Category D', path: '/shop?category=category-d' },
  { label: 'Sale', path: '/shop?tag=Sale' },
];

export default function Navbar() {
  const [scrolled, setScrolled] = useState(false);
  const [menuOpen, setMenuOpen] = useState(false);
  const [searchOpen, setSearchOpen] = useState(false);
  const location = useLocation();
  const { toggleCart, itemCount } = useCartStore();
  const count = itemCount();

  useEffect(() => {
    const onScroll = () => setScrolled(window.scrollY > 40);
    window.addEventListener('scroll', onScroll, { passive: true });
    return () => window.removeEventListener('scroll', onScroll);
  }, []);

  useEffect(() => {
    setMenuOpen(false);
  }, [location]);

  const isHome = location.pathname === '/';

  return (
    <>
      <header
        className={clsx(
          'fixed top-0 left-0 right-0 z-50 transition-all duration-300',
          scrolled || !isHome
            ? 'bg-white/95 backdrop-blur-md shadow-sm border-b border-neutral-100'
            : 'bg-black/30 backdrop-blur-sm'
        )}
      >
        <div className="max-w-screen-xl mx-auto px-4 sm:px-6">
          <div className="flex items-center justify-between h-16 md:h-20">
            {/* Mobile menu toggle */}
            <button
              className={clsx(
                'md:hidden p-2 -ml-2',
                scrolled || !isHome ? 'text-neutral-800' : 'text-white'
              )}
              onClick={() => setMenuOpen(!menuOpen)}
              aria-label="Toggle menu"
            >
              {menuOpen ? <X size={22} /> : <Menu size={22} />}
            </button>

            {/* Logo */}
            <Link
              to="/"
              className={clsx(
                'font-display font-bold text-xl md:text-2xl tracking-[0.15em] uppercase',
                scrolled || !isHome ? 'text-neutral-900' : 'text-white'
              )}
            >
              __SITE_NAME__
            </Link>

            {/* Desktop Nav */}
            <nav className="hidden md:flex items-center gap-8">
              {defaultNavLinks.map((link) => (
                <Link
                  key={link.path}
                  to={link.path}
                  className={clsx(
                    'text-xs font-medium tracking-widest uppercase transition-colors duration-150 hover:opacity-60',
                    scrolled || !isHome ? 'text-neutral-700' : 'text-white/90'
                  )}
                >
                  {link.label}
                </Link>
              ))}
            </nav>

            {/* Actions */}
            <div className="flex items-center gap-4">
              <button
                className={clsx(
                  'transition-opacity hover:opacity-60',
                  scrolled || !isHome ? 'text-neutral-800' : 'text-white'
                )}
                onClick={() => setSearchOpen(!searchOpen)}
                aria-label="Search"
              >
                <Search size={20} />
              </button>
              <Link
                to="/wishlist"
                className={clsx(
                  'transition-opacity hover:opacity-60',
                  scrolled || !isHome ? 'text-neutral-800' : 'text-white'
                )}
                aria-label="Wishlist"
              >
                <Heart size={20} />
              </Link>
              <button
                className={clsx(
                  'relative transition-opacity hover:opacity-60',
                  scrolled || !isHome ? 'text-neutral-800' : 'text-white'
                )}
                onClick={toggleCart}
                aria-label="Shopping cart"
              >
                <ShoppingBag size={20} />
                {count > 0 && (
                  <span className="absolute -top-1.5 -right-1.5 w-4 h-4 bg-neutral-900 text-white text-[10px] rounded-full flex items-center justify-center font-medium">
                    {count}
                  </span>
                )}
              </button>
            </div>
          </div>
        </div>

        {/* Search Bar */}
        <div
          className={clsx(
            'overflow-hidden transition-all duration-300 bg-white border-t border-neutral-100',
            searchOpen ? 'max-h-16' : 'max-h-0'
          )}
        >
          <div className="max-w-screen-xl mx-auto px-4 sm:px-6 py-3">
            <div className="relative">
              <Search size={16} className="absolute left-3 top-1/2 -translate-y-1/2 text-neutral-400" />
              <input
                type="text"
                placeholder="Search products..."
                className="w-full pl-9 pr-4 py-2 text-sm bg-neutral-50 border border-neutral-200 rounded-full outline-none focus:border-neutral-400 transition-colors"
                autoFocus={searchOpen}
              />
            </div>
          </div>
        </div>
      </header>

      {/* Mobile Menu Overlay */}
      <div
        className={clsx(
          'fixed inset-0 z-40 bg-white transition-transform duration-300 md:hidden flex flex-col',
          menuOpen ? 'translate-x-0' : '-translate-x-full'
        )}
      >
        <div className="flex items-center justify-between px-4 h-16 border-b border-neutral-100">
          <span className="font-display font-bold text-xl tracking-[0.15em] uppercase">__SITE_NAME__</span>
          <button onClick={() => setMenuOpen(false)} aria-label="Close menu">
            <X size={22} />
          </button>
        </div>
        <nav className="flex flex-col p-6 gap-6">
          {defaultNavLinks.map((link) => (
            <Link
              key={link.path}
              to={link.path}
              className="text-sm font-medium tracking-widest uppercase text-neutral-700 hover:text-neutral-900"
            >
              {link.label}
            </Link>
          ))}
        </nav>
      </div>

      {/* Spacer for fixed header */}
      <div className="h-16 md:h-20" />
    </>
  );
}
