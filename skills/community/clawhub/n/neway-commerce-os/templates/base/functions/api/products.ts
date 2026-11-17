// Mock catalog endpoint.
// The single source of truth for product data is `src/data/products.ts`.
// Replace the body below with a database query when you go to production —
// keep the response shape identical to the `Product` interface in `src/types/index.ts`.

type CatalogProduct = {
  id: string;
  name: string;
  nameEn?: string;
  category: string;
  price: number;
  rating: number;
  tags: string[];
  images: string[];
  isNew: boolean;
  isSale: boolean;
};

const MOCK_CATALOG: CatalogProduct[] = [
  {
    id: 'wool-blend-coat',
    name: 'Wool-Blend Long Coat',
    nameEn: 'Double-Face Wool',
    category: 'outerwear',
    price: 1980,
    rating: 4.9,
    tags: ['New', 'Bestseller'],
    images: ['/images/1539533018447.jpg'],
    isNew: true,
    isSale: true,
  },
  {
    id: 'silk-floral-dress',
    name: 'Silk Floral Dress',
    nameEn: 'Limited Print',
    category: 'dress',
    price: 1680,
    rating: 4.9,
    tags: ['New', 'Bestseller'],
    images: ['/images/1572804013427.jpg'],
    isNew: true,
    isSale: false,
  },
  {
    id: 'quilted-chain-bag',
    name: 'Quilted Chain Bag',
    nameEn: 'Two-Way Chain',
    category: 'bags',
    price: 2280,
    rating: 4.8,
    tags: ['Sale', 'Bestseller'],
    images: ['/images/1548036328.jpg'],
    isNew: false,
    isSale: true,
  },
];

export default async function handler() {
  return Response.json({
    ok: true,
    source: 'mock',
    currency: 'CNY',
    count: MOCK_CATALOG.length,
    products: MOCK_CATALOG,
  });
}
