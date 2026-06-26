#!/usr/bin/env node

import { CONFIG, getFirstEnabledProvider } from '../config.js';

async function geocodeAmap(address) {
  const url = new URL(`${CONFIG.amap.baseUrl}/geocode/geo`);
  url.searchParams.set('key', CONFIG.amap.key);
  url.searchParams.set('address', address);
  
  const response = await fetch(url.toString());
  const data = await response.json();
  
  if (data.status === '1' && data.geocodes && data.geocodes.length > 0) {
    const geo = data.geocodes[0];
    const [lng, lat] = geo.location.split(',');
    return {
      success: true,
      provider: 'amap',
      address: geo.formatted_address || address,
      location: { lng: parseFloat(lng), lat: parseFloat(lat) },
      level: geo.level,
      adcode: geo.adcode
    };
  }
  return { success: false, provider: 'amap', error: data.info || 'Geocoding failed' };
}

async function geocodeBaidu(address) {
  const url = new URL(`${CONFIG.baidu.baseUrl}/geocoding/v3/`);
  url.searchParams.set('ak', CONFIG.baidu.key);
  url.searchParams.set('address', address);
  url.searchParams.set('output', 'json');
  
  const response = await fetch(url.toString());
  const data = await response.json();
  
  if (data.status === 0 && data.result) {
    return {
      success: true,
      provider: 'baidu',
      address: address,
      location: data.result.location,
      confidence: data.result.confidence,
      level: data.result.level
    };
  }
  return { success: false, provider: 'baidu', error: data.message || 'Geocoding failed' };
}

async function geocodeTencent(address) {
  const url = new URL(`${CONFIG.tencent.baseUrl}/ws/geocoder/v1/`);
  url.searchParams.set('key', CONFIG.tencent.key);
  url.searchParams.set('address', address);
  
  const response = await fetch(url.toString());
  const data = await response.json();
  
  if (data.status === 0 && data.result) {
    return {
      success: true,
      provider: 'tencent',
      address: data.result.address || address,
      location: data.result.location,
      ad_info: data.result.ad_info
    };
  }
  return { success: false, provider: 'tencent', error: data.message || 'Geocoding failed' };
}

export async function geocode(address, provider = null) {
  const targetProvider = provider || getFirstEnabledProvider();
  
  if (!targetProvider) {
    throw new Error('No map provider configured. Please set AMAP_KEY, BAIDU_MAP_KEY, or TENCENT_MAP_KEY environment variable.');
  }
  
  switch (targetProvider) {
    case 'amap':
      return geocodeAmap(address);
    case 'baidu':
      return geocodeBaidu(address);
    case 'tencent':
      return geocodeTencent(address);
    default:
      throw new Error(`Unknown provider: ${targetProvider}`);
  }
}

async function main() {
  const args = process.argv.slice(2);
  
  if (args.length === 0) {
    console.error('Usage: node geocode.mjs <address> [--provider <amap|baidu|tencent>]');
    console.error('\nExample:');
    console.error('  node geocode.mjs "北京市朝阳区三里屯"');
    console.error('  node geocode.mjs "北京市朝阳区三里屯" --provider amap');
    process.exit(1);
  }
  
  let address = '';
  let provider = null;
  
  for (let i = 0; i < args.length; i++) {
    if (args[i] === '--provider' && args[i + 1]) {
      provider = args[i + 1];
      i++;
    } else {
      address += (address ? ' ' : '') + args[i];
    }
  }
  
  try {
    const result = await geocode(address, provider);
    console.log(JSON.stringify(result, null, 2));
  } catch (error) {
    console.error('Error:', error.message);
    process.exit(1);
  }
}

main();
