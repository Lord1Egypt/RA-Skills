export function keywordScan(code: string, patterns: any) {

    const issues: any[] = []

    for (const keyword of patterns.dangerous_keywords ?? []) {

        if (code.includes(keyword)) {

            issues.push({
                type: "keyword",
                keyword
            })

        }

    }

    for (const file of patterns.sensitive_files ?? []) {

        if (code.includes(file)) {

            issues.push({
                type: "sensitive_file",
                file
            })

        }

    }

    for (const url of patterns.suspicious_urls ?? []) {

        if (code.includes(url)) {

            issues.push({
                type: "suspicious_url",
                url
            })

        }

    }

    for (const pattern of patterns.suspicious_patterns ?? []) {

        const regex = new RegExp(pattern)

        if (regex.test(code)) {

            issues.push({
                type: "suspicious_pattern",
                pattern
            })

        }

    }

    return issues

}