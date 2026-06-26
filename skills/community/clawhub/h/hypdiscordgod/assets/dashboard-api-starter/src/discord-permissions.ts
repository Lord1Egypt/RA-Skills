export function hasManageGuildPermission(permissionBits: string | number | bigint): boolean {
  const perms = BigInt(permissionBits);
  const MANAGE_GUILD = 1n << 5n;
  const ADMINISTRATOR = 1n << 3n;
  return (perms & MANAGE_GUILD) === MANAGE_GUILD || (perms & ADMINISTRATOR) === ADMINISTRATOR;
}
