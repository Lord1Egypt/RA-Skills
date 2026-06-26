#!/usr/bin/env node

import { CONFIG, getFirstEnabledProvider } from '../config.js';
import { geocode } from './geocode.mjs';

async function searchPromotionsAmap(location, options = {}) {
  const { radius = 5000, limit = 20 } = options;
  const url = new URL(`${CONFIG.amap.baseUrl}/place/around`);
  
  url.searchParams.set('key', CONFIG.amap.key);
  url.searchParams.set('location', `${location.lng},${location.lat}`);
  url.searchParams.set('radius', radius.toString());
  url.searchParams.set('offset', limit.toString());
  url.searchParams.set('keywords', '优惠|促销|折扣|活动|开业');
  url.searchParams.set('extensions', 'all');
  
  const response = await fetch(url.toString());
  const data = await response.json();
  
  if (data.status === '1' && data.pois) {
    return {
      success: true,
      provider: 'amap',
      searchType: 'promotion',
      count: data.pois.length,
      promotions: data.pois.map(poi => ({
        id: poi.id,
        name: poi.name,
        address: poi.address,
        distance: poi.distance,
        tel: poi.tel,
        type: poi.type,
        biz_ext: poi.biz_ext
      })).filter(p => p.biz_ext || p.type)
    };
  }
  return { success: false, provider: 'amap', error: data.info || 'Search failed' };
}

async function searchPromotionsBaidu(location, options = {}) {
  const { radius = 5000, limit = 20 } = options;
  const url = new URL(`${CONFIG.baidu.baseUrl}/place/v2/search`);
  
  url.searchParams.set('ak', CONFIG.baidu.key);
  url.searchParams.set('location', `${location.lat},${location.lng}`);
  url.searchParams.set('radius', radius.toString());
  url.searchParams.set('output', 'json');
  url.searchParams.set('page_size', limit.toString());
  url.searchParams.set('query', '优惠促销');
  url.searchParams.set('scope', '2');
  
  const response = await fetch(url.toString());
  const data = await response.json();
  
  if (data.status === 0 && data.results) {
    return {
      success: true,
      provider: 'baidu',
      searchType: 'promotion',
      count: data.results.length,
      promotions: data.results.map(poi => ({
        id: poi.uid,
        name: poi.name,
        address: poi.address,
        distance: poi.detail_info?.distance,
        tel: poi.telephone,
        type: poi.detail_info?.tag,
        detail: poi.detail_info
      }))
    };
  }
  return { success: false, provider: 'baidu', error: data.message || 'Search failed' };
}

async function searchPromotionsTencent(location, options = {}) {
  const { radius = 5000, limit = 20 } = options;
  const url = new URL(`${CONFIG.tencent.baseUrl}/ws/place/v1/explore`);
  
  url.searchParams.set('key', CONFIG.tencent.key);
  url.searchParams.set('boundary', `nearby(${location.lat},${location.lng},${radius})`);
  url.searchParams.set('page_size', limit.toString());
  url.searchParams.set('keyword', '优惠 促销 折扣');
  
  const response = await fetch(url.toString());
  const data = await response.json();
  
  if (data.status === 0 && data.data) {
    return {
      success: true,
      provider: 'tencent',
      searchType: 'promotion',
      count: data.data.length,
      promotions: data.data.map(poi => ({
        id: poi.id,
        name: poi.title,
        address: poi.address,
        distance: poi._distance,
        tel: poi.tel,
        type: poi.category
      }))
    };
  }
  return { success: false, provider: 'tencent', error: data.message || 'Search failed' };
}

export async function searchPromotions(address, options = {}) {
  const provider = options.provider || getFirstEnabledProvider();
  
  if (!provider) {
    throw new Error('No map provider configured. Please set AMAP_KEY, BAIDU_MAP_KEY, or TENCENT_MAP_KEY environment variable.');
  }
  
  const geoResult = await geocode(address, provider);
  if (!geoResult.success) {
    return geoResult;
  }
  
  const location = geoResult.location;
  
  switch (provider) {
    case 'amap':
      return searchPromotionsAmap(location, options);
    case 'baidu':
      return searchPromotionsBaidu(location, options);
    case 'tencent':
      return searchPromotionsTencent(location, options);
    default:
      throw new Error(`Unknown provider: ${provider}`);
  }
}

async function main() {
  const args = process.argv.slice(2);
  
  if (args.length === 0) {
    console.error('Usage: node promotion.mjs <address> [options]');
    console.error('\nOptions:');
    console.error('  --radius <meters>   Search radius (default: 5000)');
    console.error('  --limit <count>     Max results (default: 20)');
    console.error('  --provider <name>   Map provider (amap, baidu, tencent)');
    console.error('\nExample:');
    console.error('  node promotion.mjs "北京市朝阳区三里屯" --radius 3000');
    process.exit(1);
  }
  
  const options = { radius: 5000, limit: 20 };
  let address = '';
  
  for (let i = 0; i < args.length; i++) {
    if (args[i] === '--radius' && args[i + 1]) {
      options.radius = parseInt(args[i + 1], 10);
      i++;
    } else if (args[i] === '--limit' && args[i + 1]) {
      options.limit = parseInt(args[i + 1], 10);
      i++;
    } else if (args[i] === '--provider' && args[i + 1]) {
      options.provider = args[i + 1];
      i++;
    } else {
      address += (address ? ' ' : '') + args[i];
    }
  }
  
  try {
    const result = await searchPromotions(address, options);
    console.log(JSON.stringify(result, null, 2));
  } catch (error) {
    console.error('Error:', error.message);
    process.exit(1);
  }
}

main();
