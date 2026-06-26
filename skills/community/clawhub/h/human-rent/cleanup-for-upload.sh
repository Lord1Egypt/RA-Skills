#!/bin/bash
#
# ClawHub Upload Cleanup Script
# Removes internal documentation files before upload
#
# Run this script from the human-rent directory:
#   cd /www/wwwroot/docs.zhenrent.com/human-rent
#   bash cleanup-for-upload.sh
#

set -e

echo "=========================================="
echo "ClawHub Upload Cleanup Script"
echo "human-rent v0.2.1"
echo "=========================================="
echo ""

# Verify we're in the right directory
if [ ! -f "_meta.json" ] || [ ! -f "package.json" ]; then
    echo "ERROR: Must run from human-rent directory"
    exit 1
fi

echo "Current directory: $(pwd)"
echo ""

# Count files before cleanup
BEFORE=$(find . -type f | wc -l)
echo "Files before cleanup: $BEFORE"
echo ""

# Show files that will be removed
echo "Files to be removed (internal documentation):"
echo "  - CLAWHUB-SUBMISSION.md"
echo "  - FINAL_UPLOAD_GUIDE.md"
echo "  - QUICK-UPLOAD-GUIDE.txt"
echo "  - QUICK_STATUS.txt"
echo "  - UPLOAD-READY.md"
echo "  - UPLOAD_CHECKLIST.txt"
echo "  - VERIFICATION_REPORT.md"
echo "  - FILE_ANALYSIS.txt"
echo "  - cleanup-for-upload.sh (this script)"
echo ""

# Ask for confirmation
read -p "Proceed with cleanup? (y/N): " -n 1 -r
echo ""

if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "Cleanup cancelled."
    exit 0
fi

# Remove internal documentation files
echo "Removing internal documentation files..."
rm -f CLAWHUB-SUBMISSION.md
rm -f FINAL_UPLOAD_GUIDE.md
rm -f QUICK-UPLOAD-GUIDE.txt
rm -f QUICK_STATUS.txt
rm -f UPLOAD-READY.md
rm -f UPLOAD_CHECKLIST.txt
rm -f VERIFICATION_REPORT.md
rm -f FILE_ANALYSIS.txt

# Count files after cleanup
AFTER=$(find . -type f | wc -l)
echo "Files after cleanup: $AFTER"
echo "Files removed: $((BEFORE - AFTER - 1))"  # -1 for this script itself
echo ""

# Show final size
SIZE=$(du -sh . | cut -f1)
echo "Package size: $SIZE"
echo ""

# Show remaining files
echo "Remaining files:"
find . -type f | sort
echo ""

echo "=========================================="
echo "Cleanup complete!"
echo "=========================================="
echo ""
echo "Next steps:"
echo "1. Review remaining files above"
echo "2. Test CLI: ./bin/human-rent --version"
echo "3. Upload folder to ClawHub:"
echo "   https://clawhub.ai/zhenstaff/human-rent"
echo ""

# Self-destruct (remove this script)
echo "Removing cleanup script..."
rm -f cleanup-for-upload.sh
echo "Done!"
