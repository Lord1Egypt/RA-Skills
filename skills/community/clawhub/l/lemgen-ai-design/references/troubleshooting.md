# Troubleshooting

## Free tools work but generation fails

Set `LEMGEN_API_TOKEN` in your MCP host config and restart the host.

## No prompt results

Update the package or refresh `data/trending-prompts.json` from
`lemgen-trending-prompts`.

## Video times out

Do not retry immediately. Check the generation history at `https://lemgen.org`
because a video job may still be running.
