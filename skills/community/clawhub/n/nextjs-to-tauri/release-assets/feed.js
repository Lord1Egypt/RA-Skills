import { requireValue, safeName } from './common.js';
export function resolveAsset(url, {repo, tag, assets}) {
  const parsed = new URL(url);
  requireValue(parsed.protocol === 'https:' && !parsed.port && !parsed.username && !parsed.password, 'Invalid asset URL');
  const apiPrefix = ("/repos/" + (repo) + "/releases/assets/");
  if (parsed.hostname === 'api.github.com' && parsed.pathname.startsWith(apiPrefix)) {
    const id = parsed.pathname.slice(apiPrefix.length);
    requireValue(/^\d+$/.test(id), 'Invalid asset ID');
    const found = assets.filter(asset => String(asset.id) === id);
    requireValue(found.length === 1, 'Asset ID does not belong to this draft');
    requireValue(safeName(found[0].name), 'Unsafe asset name');
    return found[0].name;
  }
  const prefix = ("/" + (repo) + "/releases/download/" + (tag) + "/");
  requireValue(parsed.hostname === 'github.com' && parsed.pathname.startsWith(prefix), 'Unexpected asset repository or tag');
  const name = decodeURIComponent(parsed.pathname.slice(prefix.length));
  requireValue(safeName(name) && assets.some(asset => asset.name === name), 'Unknown draft asset');
  return name;
}

export function verifyFeed(feed, {version, repo, tag, assets, files, signatures, preferNsis = false}) {
  requireValue(feed.version === version && feed.platforms && typeof feed.platforms === 'object' && Object.keys(feed.platforms).length > 0, 'Updater version or platforms mismatch');
  for (const [platform, entry] of Object.entries(feed.platforms)) {
    const match = /^(windows|darwin|linux)-(x86_64|aarch64)(?:-(nsis|msi|app|appimage|deb|rpm))?$/.exec(platform);
    requireValue(match, ("Unknown updater platform " + (platform)));
    const name = resolveAsset(entry.url, {repo, tag, assets});
    requireValue(files.has(name), ("" + (platform) + " references an unbuilt asset " + (name)));
    const arch = match[2] === 'aarch64' ? /(^|[-_.])(arm64|aarch64)([-_.]|$)/i : /(^|[-_.])(amd64|x64|x86_64)([-_.]|$)/i;
    requireValue(arch.test(name), ("" + (platform) + " architecture mismatch"));
    const types = {windows: /(?:[-_]setup\.exe|\.nsis\.zip|\.msi(?:\.zip)?)$/i,
      darwin: /\.app\.tar\.gz$/i, linux: /\.AppImage(?:\.tar\.gz)?$/i};
    const bundles = {nsis: /(?:[-_]setup\.exe|\.nsis\.zip)$/i, msi: /\.msi(?:\.zip)?$/i,
      app: /\.app\.tar\.gz$/i, appimage: /\.AppImage(?:\.tar\.gz)?$/i, deb: /\.deb$/i, rpm: /\.rpm$/i};
    requireValue((match[3] ? bundles[match[3]] : types[match[1]]).test(name), ("" + (platform) + " artifact type mismatch"));
    if (preferNsis && match[1] === 'windows' && !match[3]) requireValue(bundles.nsis.test(name), ("" + (platform) + " must use NSIS"));
    requireValue(!match[3] || ({windows: ['nsis', 'msi'], darwin: ['app'], linux: ['appimage', 'deb', 'rpm']})[match[1]].includes(match[3]), ("" + (platform) + " bundle mismatch"));
    requireValue(files.has(name + '.sig') && typeof entry.signature === 'string' && entry.signature.trim() &&
      signatures.get(name + '.sig')?.trim() === entry.signature.trim(), ("" + (platform) + " signature mismatch"));
  }
}
