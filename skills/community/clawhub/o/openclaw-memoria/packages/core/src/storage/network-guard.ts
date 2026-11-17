/**
 * Garde anti-réseau (décision D1) : détecter qu'un chemin vit sur un volume
 * réseau ou synchronisé (NAS SMB/NFS, iCloud Drive, Dropbox, Google Drive…)
 * où le mode WAL de SQLite risque la corruption.
 *
 * Heuristiques volontairement simples et sans dépendance :
 *  - macOS : tout ce qui vit sous /Volumes/* (hors disque de démarrage),
 *    `~/Library/Mobile Documents` (iCloud), dossiers CloudStorage.
 *  - Linux : préfixes de montage réseau courants (/mnt, /media, /net, /smb).
 *  - Windows : lecteurs UNC (\\serveur\...).
 * `statfs` confirme quand l'API est disponible (Node ≥ 18.15).
 */
import { statfsSync } from 'node:fs'
import { homedir, platform } from 'node:os'
import { resolve, sep } from 'node:path'

const NETWORK_FS_TYPES = new Set([
  'nfs', 'nfs4', 'smbfs', 'cifs', 'afpfs', 'webdav', 'fuse.sshfs', 'fuse', '9p', 'ncpfs',
])

// fs type magic numbers (Linux statfs.type) des FS réseau les plus courants
const NETWORK_FS_MAGIC = new Set([
  0x6969, // NFS_SUPER_MAGIC
  0xff534d42, // CIFS / SMB
  0xfe534d42, // SMB2
  0x517b, // SMB classique
  0x65735546, // FUSE
])

export function isOnNetworkVolume(path: string): boolean {
  const p = resolve(path)
  const home = homedir()

  if (platform() === 'win32') {
    return p.startsWith('\\\\')
  }

  // iCloud Drive / fournisseurs cloud macOS
  if (p.startsWith(`${home}/Library/Mobile Documents`)) return true
  if (p.startsWith(`${home}/Library/CloudStorage`)) return true
  // Dropbox / Google Drive par convention de chemin
  if (p.includes(`${sep}Dropbox${sep}`) || p.endsWith(`${sep}Dropbox`)) return true

  // Volumes montés (macOS) — le disque de démarrage n'apparaît pas sous /Volumes pour les chemins usuels
  if (platform() === 'darwin' && p.startsWith('/Volumes/')) return true

  // Montages réseau usuels Linux
  if (platform() === 'linux' && (/^\/(mnt|media|net|smb)\//.test(p))) {
    // un /mnt local n'est pas forcément réseau → on confirme via statfs si possible
    return statfsSaysNetwork(p) ?? true
  }

  return statfsSaysNetwork(p) ?? false
}

function statfsSaysNetwork(path: string): boolean | null {
  try {
    const st = statfsSync(path)
    if (NETWORK_FS_MAGIC.has(st.type)) return true
    // certains runtimes exposent un nom plutôt qu'un magic — défensif
    const typeName = String((st as unknown as { typeName?: string }).typeName ?? '').toLowerCase()
    if (typeName && NETWORK_FS_TYPES.has(typeName)) return true
    return false
  } catch {
    return null
  }
}
