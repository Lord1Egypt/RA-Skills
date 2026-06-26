export interface CompanyData {
  name: string;
  registration_number: string;
  type: string;
  status: string;
  incorporation_date: string;
  address: string;
  directors: string[];
  nature_of_business: string;
}

export interface LookupParams {
  query: string;
  type?: "name" | "registration_number";
  fetchFn?: typeof fetch;
}

export function detectQueryType(query: string): "name" | "registration_number" {
  if (/^\d{12}$/.test(query.trim())) return "registration_number";
  if (/^\d+-[A-Z]$/i.test(query.trim())) return "registration_number";
  return "name";
}

const SSM_API_BASE = "https://ssm-api.swmengappdev.workers.dev";

export async function lookupCompany(params: LookupParams): Promise<CompanyData> {
  const { query, fetchFn = fetch } = params;
  const type = params.type ?? detectQueryType(query);

  const url = `${SSM_API_BASE}/lookup?${type === "name" ? "name" : "reg_no"}=${encodeURIComponent(query)}`;

  const response = await fetchFn(url);

  if (!response.ok) {
    const err = await response.json() as { error: string };
    throw new Error(err.error ?? `Lookup failed with status ${response.status}`);
  }

  return response.json() as Promise<CompanyData>;
}
