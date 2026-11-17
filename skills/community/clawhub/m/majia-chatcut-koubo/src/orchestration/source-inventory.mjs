export class SourceInventoryError extends Error {
  constructor(code, message) {
    super(message);
    this.name = "SourceInventoryError";
    this.code = code;
  }
}

export function assertSourceInventoryBindings(inventory) {
  const refs = (inventory?.assets ?? []).map((item) => item.logicalRef);
  if (refs.length !== new Set(refs).size) {
    throw new SourceInventoryError(
      "SOURCE_LOGICAL_REF_DUPLICATE",
      "source inventory logical references must be unique",
    );
  }
  const mainMatches = refs.filter((ref) => ref === inventory?.mainSourceRef);
  if (mainMatches.length !== 1) {
    throw new SourceInventoryError(
      "SOURCE_MAIN_REF_UNRESOLVED",
      "main source reference must resolve to exactly one asset",
    );
  }
  return true;
}
