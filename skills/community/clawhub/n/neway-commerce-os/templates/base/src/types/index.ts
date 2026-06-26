export interface Product {
  id: string;
  name: string;
  nameEn?: string;
  brand: string;
  category: string;
  price: number;
  originalPrice?: number;
  images: string[];
  colors: { name: string; hex: string }[];
  sizes: string[];
  description: string;
  details: string[];
  tags: string[];
  rating: number;
  reviewCount: number;
  isNew: boolean;
  isSale: boolean;
  material?: string;
  fit?: string;
}

export interface Category {
  key: string;
  label: string;
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
