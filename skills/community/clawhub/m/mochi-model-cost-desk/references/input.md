# Action contract

estimate: file (CSV headers model,input_tokens,cached_input_tokens,output_tokens); ratesAsOf (string identifying rate date/source); rates:[{model,currency,inputPerMillion,cachedInputPerMillion,outputPerMillion}]; budget:{USD:"10",CNY:"50"} optional. input_tokens includes cached tokens, so uncached=input-cached. Counts are integer strings; rates are nonnegative decimals per million tokens. Missing rates or cached>input fail. Never merges currencies or guesses exchange rates.

## Request example

```json
{
  "action": "estimate",
  "file": "samples/usage.csv",
  "ratesAsOf": "Fictional sample, not provider pricing",
  "rates": [
    {
      "model": "demo-model",
      "currency": "USD",
      "inputPerMillion": "2",
      "cachedInputPerMillion": ".2",
      "outputPerMillion": "8"
    }
  ],
  "budget": {
    "USD": "5"
  }
}
```

## Runtime and boundaries

Python 3.10+ standard library. Paths must be relative to the active workspace; absolute paths, parent traversal, symbolic links and junctions are rejected. This is a path guard, not OS-level isolation: retain the host container/sandbox. A helper field does not grant permission to access another account or send information.

Ask for the provider’s current rate units and whether input includes cached tokens. Save the rate date/source. Estimates are not official invoices, and do not include tool, search, storage, tax or other charges unless already represented by the supplied data.
