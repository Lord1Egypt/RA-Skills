
export const CONFIG = {
  amap: {
    key: process.env.AMAP_KEY || '',
    baseUrl: 'https://restapi.amap.com/v3',
    enabled: !!process.env.AMAP_KEY
  },
  baidu: {
    key: process.env.BAIDU_MAP_KEY || '',
    baseUrl: 'https://api.map.baidu.com',
    enabled: !!process.env.BAIDU_MAP_KEY
  },
  tencent: {
    key: process.env.TENCENT_MAP_KEY || '',
    baseUrl: 'https://apis.map.qq.com',
    enabled: !!process.env.TENCENT_MAP_KEY
  }
};

export function getEnabledProviders() {
  return Object.entries(CONFIG)
    .filter(([_, config]) =&gt; config.enabled)
    .map(([name]) =&gt; name);
}

export function getFirstEnabledProvider() {
  const providers = getEnabledProviders();
  return providers[0] || null;
}
