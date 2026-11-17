import type { LucideIcon } from 'lucide-react';

export interface Product {
  id: string; // URL-safe slug, used by /product/:id
  name: string; // primary display name
  nameEn?: string; // optional secondary line — a short subtitle or the Latin name
  brand: string;
  category: string; // must match a Category.key
  price: number; // current price
  originalPrice?: number; // crossed-out price
  unit?: string; // e.g. 'item' / 'set' — omit when not applicable
  images: string[]; // at least 2 — [0] primary, [1] used for hover swap
  colors: { name: string; hex: string }[];
  sizes: string[];
  description: string; // full paragraph
  details: string[]; // feature bullet list
  highlight: string; // one-line selling point shown on ProductCard
  tags: string[]; // shop filter tags, e.g. ['New', 'Bestseller']
  material: string;
  fit: string;
  rating: number; // 0–5
  reviewCount: number;
  stock: number; // <= 10 renders the LOW STOCK badge
  isNew: boolean;
  isSale: boolean;
}

export interface Category {
  key: string; // 'all' plus one key per real category
  label: string;
  icon: LucideIcon; // lucide line icon
  image: string; // banner image, local `/images/*.jpg` or verified remote URL
}

export interface CartItem {
  product: Product;
  selectedSize: string;
  selectedColor: string;
  quantity: number;
}

export interface PromoCode {
  code: string;
  discount: number;
  type: 'percent' | 'fixed';
  description: string;
}
