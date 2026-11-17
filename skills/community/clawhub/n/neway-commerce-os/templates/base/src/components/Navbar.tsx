import { useEffect, useState } from 'react';
import { Link, useLocation } from 'react-router-dom';
import { Heart, Menu, Search, ShoppingBag, X } from 'lucide-react';
import { useCartStore } from '../store/cartStore';
import { categories } from '../data/products';
import clsx from 'clsx';

const tagLinks = [
  { label: 'New', path: '/shop?tag=New' },
  { label: 'Sale', path: '/shop?tag=Sale' },
];

export default function Navbar() {
  const [scrolled, setScrolled] = useState(false);
  const [menuOpen, setMenuOpen] = useState(false);
  const [searchOpen, setSearchOpen] = useState(false);
  const location = useLocation();
  const { toggleCart, itemCount } = useCartStore();
  const count = itemCount();

  const categoryLinks = categories
    .filter((c) => c.key !== 'all')
    .map((c) => ({ label: c.label, path: `/shop?category=${c.key}` }));

  const navLinks = [...categoryLinks, ...tagLinks];

  useEffect(() => {
    const onScroll = () => setScrolled(window.scrollY > 40);
    window.addEventListener('scroll', onScroll, { passive: true });
    return () => window.removeEventListener('scroll', onScroll);
  }, []);

  useEffect(() => {
    setMenuOpen(false);
  }, [location]);

  const isHome = location.pathname === '/';
  const onDark = !scrolled && isHome;

  return (
    <>
      <header
        className={clsx(
          'fixed top-0 left-0 right-0 z-50 transition-all duration-300',
          onDark
            ? 'bg-black/30 backdrop-blur-sm'
            : 'border-b border-neutral-100 bg-white/95 backdrop-blur-md shadow-sm'
        )}
      >
        <div className="mx-auto max-w-screen-xl px-4 sm:px-6">
          <div className="flex h-16 items-center justify-between md:h-20">
            {/* Mobile menu toggle */}
            <button
              className={clsx('p-2 -ml-2 md:hidden', onDark ? 'text-white' : 'text-neutral-800')}
              onClick={() => setMenuOpen(!menuOpen)}
              aria-label="Open menu"
            >
              {menuOpen ? <X size={22} /> : <Menu size={22} />}
            </button>

            {/* Logo */}
            <Link
              to="/"
              className={clsx(
                'font-display text-xl font-bold uppercase tracking-[0.15em] md:text-2xl',
                onDark ? 'text-white' : 'text-neutral-900'
              )}
            >
              __SITE_NAME__
            </Link>

            {/* Desktop nav */}
            <nav className="hidden items-center gap-7 md:flex">
              {navLinks.map((link) => (
                <Link
                  key={link.path}
                  to={link.path}
                  className={clsx(
                    'text-xs font-medium tracking-widest transition-colors duration-150 hover:opacity-60',
                    onDark ? 'text-white/90' : 'text-neutral-700'
                  )}
                >
                  {link.label}
                </Link>
              ))}
            </nav>

            {/* Actions */}
            <div className="flex items-center gap-4">
              <button
                className={clsx('transition-opacity hover:opacity-60', onDark ? 'text-white' : 'text-neutral-800')}
                onClick={() => setSearchOpen(!searchOpen)}
                aria-label="Search"
              >
                <Search size={20} />
              </button>
              <Link
                to="/wishlist"
                className={clsx('transition-opacity hover:opacity-60', onDark ? 'text-white' : 'text-neutral-800')}
                aria-label="Wishlist"
              >
                <Heart size={20} />
              </Link>
              <button
                className={clsx('relative transition-opacity hover:opacity-60', onDark ? 'text-white' : 'text-neutral-800')}
                onClick={toggleCart}
                aria-label="Cart"
              >
                <ShoppingBag size={20} />
                {count > 0 && (
                  <span className="absolute -right-1.5 -top-1.5 flex h-4 w-4 items-center justify-center rounded-full bg-brand-600 text-[12px] font-medium text-white">
                    {count}
                  </span>
                )}
              </button>
            </div>
          </div>
        </div>

        {/* Search bar */}
        <div
          className={clsx(
            'overflow-hidden border-t border-neutral-100 bg-white transition-all duration-300',
            searchOpen ? 'max-h-16' : 'max-h-0'
          )}
        >
          <div className="mx-auto max-w-screen-xl px-4 py-3 sm:px-6">
            <div className="relative">
              <Search size={16} className="absolute left-3 top-1/2 -translate-y-1/2 text-neutral-400" />
              <input
                type="text"
                placeholder="Search products..."
                className="input-field pl-9"
                autoFocus={searchOpen}
              />
            </div>
          </div>
        </div>
      </header>

      {/* Mobile menu */}
      <div
        className={clsx(
          'fixed inset-0 z-40 flex flex-col bg-white transition-transform duration-300 md:hidden',
          menuOpen ? 'translate-x-0' : '-translate-x-full'
        )}
      >
        <div className="flex h-16 items-center justify-between border-b border-neutral-100 px-4">
          <span className="font-display text-xl font-bold uppercase tracking-[0.15em]">__SITE_NAME__</span>
          <button onClick={() => setMenuOpen(false)} aria-label="Close menu">
            <X size={22} />
          </button>
        </div>
        <nav className="flex flex-col gap-6 p-6">
          {navLinks.map((link) => (
            <Link
              key={link.path}
              to={link.path}
              className="text-sm font-medium tracking-widest text-neutral-700 hover:text-brand-600"
            >
              {link.label}
            </Link>
          ))}
        </nav>
      </div>

      {/* Spacer for the fixed header */}
      <div className="h-16 md:h-20" />
    </>
  );
}
