# Troubleshooting

## Java not found
- Verify: java -version
- Install Java 11+
- Reopen terminal on Windows and verify PATH

## Hybrid backend not responding
- Start: opendataloader-pdf-hybrid --port 5002
- Check firewall/port
- Validate URL with --hybrid-url if needed

## Slow processing
- Run in batches
- Increase --hybrid-timeout for heavy OCR
- Check available RAM for backend

## Mixed columns
- Use default reading mode (xycut)
- Try --use-struct-tree on tagged PDFs

## Poor table quality
- Use json format
- Enable --hybrid docling-fast
