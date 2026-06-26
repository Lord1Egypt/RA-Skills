export type SSTType = "service" | "sales" | "tourism";
export type TaxType = "MY_SST" | "SG_GST" | "UNKNOWN";

const SST_RATES: Record<SSTType, number> = {
  service: 0.06,
  sales: 0.10,
  tourism: 0.08,
};

const SG_GST_RATE = 0.09;

export function calculateSST(amount: number, type: SSTType): number {
  return Math.round(amount * SST_RATES[type] * 100) / 100;
}

export function calculateGST(amount: number): number {
  return Math.round(amount * SG_GST_RATE * 100) / 100;
}

export function detectTaxType(text: string): TaxType {
  if (/SST\s*(No|Reg)/i.test(text)) return "MY_SST";
  if (/GST\s*(Reg|No)/i.test(text)) return "SG_GST";
  return "UNKNOWN";
}
