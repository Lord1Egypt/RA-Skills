#!/bin/bash

echo "Testing PDF Vision Skill..."
echo "=========================="

# Test with the class schedule PDF
PDF_PATH="/home/lpq/.openclaw/workspace/林佩权课表.pdf"

if [[ -f "$PDF_PATH" ]]; then
    echo "Testing with: $PDF_PATH"
    ./scripts/pdf_vision.py --pdf-path "$PDF_PATH" --prompt "Briefly summarize this document in one sentence." --output /tmp/pdf_vision_test_result.txt
    
    if [[ $? -eq 0 ]]; then
        echo "✅ Test passed!"
        echo "Result:"
        cat /tmp/pdf_vision_test_result.txt
    else
        echo "❌ Test failed!"
    fi
else
    echo "⚠️ Test PDF not found at $PDF_PATH"
    echo "Skipping test..."
fi