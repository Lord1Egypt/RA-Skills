package gwt

import (
	"fmt"
	"strconv"
	"strings"
)

type FileSearchResult struct {
	CompanyCode      string `json:"companyCode"`
	ClientIdentifier string `json:"clientIdentifier"`
	ClientReference  string `json:"clientReference"`
	Currency         string `json:"currency"`
	FileIdentifier   string `json:"fileIdentifier"`
	FileReference    string `json:"fileReference"`
	PartyName        string `json:"partyName"`
	Status           string `json:"status"`
	TravelDate       string `json:"travelDate"`
}

type FileSearchResponse struct {
	Count   int                `json:"count"`
	Results []FileSearchResult `json:"results"`
}

type ItineraryItem struct {
	VoucherIdentifier     string `json:"voucherIdentifier"`
	Date                  string `json:"date"`
	TransactionIdentifier string `json:"transactionIdentifier"`
	Supplier              string `json:"supplier"`
	Status                string `json:"status"`
	ConfirmationNumber    string `json:"confirmationNumber"`
	Location              string `json:"location"`
	Description           string `json:"description"`
}

type ItineraryResponse struct {
	Type             string          `json:"type"`
	PartyName        string          `json:"partyName"`
	FileReference    string          `json:"fileReference"`
	FileIdentifier   string          `json:"fileIdentifier"`
	ClientIdentifier string          `json:"clientIdentifier"`
	AgentReference   string          `json:"agentReference"`
	ItineraryCount   int             `json:"itineraryCount"`
	Itineraries      []ItineraryItem `json:"itineraries"`
}

type FileDocument struct {
	FileIdentifier        string `json:"fileIdentifier"`
	TransactionIdentifier string `json:"transactionIdentifier"`
	DocumentIdentifier    string `json:"documentIdentifier"`
	DocumentName          string `json:"documentName"`
	DocumentType          string `json:"documentType"`
	AttachmentURL         string `json:"attachmentUrl"`
}

type FileDocumentsResponse struct {
	Count   int            `json:"count"`
	Results []FileDocument `json:"results"`
}

func ParseGWTArray(arrayStr string) ([]interface{}, error) {
	arrayStr = strings.Trim(arrayStr, "[]")
	if arrayStr == "" {
		return []interface{}{}, nil
	}

	var result []interface{}
	var current strings.Builder
	var inString bool
	var quoteChar byte
	var depth int

	for i := 0; i < len(arrayStr); i++ {
		char := arrayStr[i]

		if inString {
			current.WriteByte(char)
			if char == quoteChar {
				bsCount := 0
				for j := i - 1; j >= 0 && arrayStr[j] == '\\'; j-- {
					bsCount++
				}
				if bsCount%2 == 0 {
					inString = false
				}
			}
			continue
		}

		switch char {
		case '\'', '"':
			inString = true
			quoteChar = char
			current.WriteByte(char)
		case '[':
			depth++
			current.WriteByte(char)
		case ']':
			depth--
			current.WriteByte(char)
		case ',':
			if depth == 0 {
				element := strings.TrimSpace(current.String())
				if element != "" {
					parsed, err := parseGWTElement(element)
					if err != nil {
						return nil, fmt.Errorf("failed to parse element '%s': %w", element, err)
					}
					result = append(result, parsed)
				}
				current.Reset()
			} else {
				current.WriteByte(char)
			}
		default:
			current.WriteByte(char)
		}
	}

	element := strings.TrimSpace(current.String())
	if element != "" {
		parsed, err := parseGWTElement(element)
		if err != nil {
			return nil, fmt.Errorf("failed to parse last element '%s': %w", element, err)
		}
		result = append(result, parsed)
	}

	return result, nil
}

func parseGWTElement(element string) (interface{}, error) {
	element = strings.TrimSpace(element)

	if (strings.HasPrefix(element, "'") && strings.HasSuffix(element, "'")) ||
		(strings.HasPrefix(element, "\"") && strings.HasSuffix(element, "\"")) {
		content := element[1 : len(element)-1]
		if strings.HasPrefix(element, "'") {
			content = strings.ReplaceAll(content, "''", "'")
		} else {
			content = strings.ReplaceAll(content, "\"\"", "\"")
		}
		return content, nil
	}

	if num, err := strconv.Atoi(element); err == nil {
		return num, nil
	}

	if num, err := strconv.ParseFloat(element, 64); err == nil {
		return num, nil
	}

	if strings.HasPrefix(element, "[") && strings.HasSuffix(element, "]") {
		return ParseGWTArray(element)
	}

	return element, nil
}

func unescapeGWT(s string) string {
	s = strings.Trim(s, "\"")

	var result strings.Builder
	for i := 0; i < len(s); i++ {
		if s[i] != '\\' || i+1 >= len(s) {
			result.WriteByte(s[i])
			continue
		}
		switch s[i+1] {
		case 'u':
			if i+5 < len(s) {
				hexStr := s[i+2 : i+6]
				if val, err := strconv.ParseUint(hexStr, 16, 32); err == nil {
					result.WriteRune(rune(val))
					i += 5
					continue
				}
			}
		case 'x':
			if i+3 < len(s) {
				hexStr := s[i+2 : i+4]
				if val, err := strconv.ParseUint(hexStr, 16, 8); err == nil {
					result.WriteByte(byte(val))
					i += 3
					continue
				}
			}
		case 'n':
			result.WriteByte('\n')
			i++
			continue
		case 'r':
			result.WriteByte('\r')
			i++
			continue
		case 't':
			result.WriteByte('\t')
			i++
			continue
		case '\\':
			result.WriteByte('\\')
			i++
			continue
		case '"':
			result.WriteByte('"')
			i++
			continue
		}
		result.WriteByte(s[i])
	}
	return result.String()
}

func ParseFileSearchResponse(responseBody string) (*FileSearchResponse, error) {
	if !strings.HasPrefix(responseBody, "//OK") {
		return nil, fmt.Errorf("response body missing //OK")
	}

	body := strings.TrimPrefix(responseBody, "//OK")
	parsedArray, err := ParseGWTArray(body)
	if err != nil {
		return nil, fmt.Errorf("failed to parse main array: %w", err)
	}

	if len(parsedArray) < 4 {
		return nil, fmt.Errorf("response too short: %d items", len(parsedArray))
	}

	dataArray, ok := parsedArray[len(parsedArray)-3].([]interface{})
	if !ok {
		return nil, fmt.Errorf("expected data array")
	}

	arraySize := 0
	if len(parsedArray) >= 6 {
		if s, ok := parsedArray[len(parsedArray)-6].(int); ok {
			arraySize = s
		} else if s, ok := parsedArray[len(parsedArray)-5].(int); ok {
			arraySize = s
		}
	} else if len(parsedArray) >= 5 {
		if s, ok := parsedArray[len(parsedArray)-5].(int); ok {
			arraySize = s
		}
	}

	oneBasedIndex, ok := parsedArray[len(parsedArray)-4].(int)
	if !ok {
		return nil, fmt.Errorf("expected one-based index")
	}

	mappedFirstStringValue, ok := dataArray[oneBasedIndex-1].(string)
	if !ok {
		return nil, fmt.Errorf("expected string value at index %d", oneBasedIndex-1)
	}

	response := FileSearchResponse{
		Count:   arraySize,
		Results: make([]FileSearchResult, 0, arraySize),
	}

	if strings.HasPrefix(mappedFirstStringValue, GWTTypeArray) {
		for i := len(parsedArray) - 6; i >= 0; i-- {
			if idx, ok := parsedArray[i].(int); ok {
				if idx <= 0 || idx >= len(dataArray) {
					continue
				}

				currentValue := dataArray[idx-1]
				if currentStringValue, ok := currentValue.(string); ok && strings.HasPrefix(currentStringValue, GWTTypeFileSearchResults) {
					result := FileSearchResult{
						ClientIdentifier: getString(parsedArray, i-2),
						ClientReference:   getDataString(dataArray, getInt(parsedArray, i-3)),
						Currency:         getDataString(dataArray, getInt(parsedArray, i-4)),
						FileIdentifier:   getString(parsedArray, i-5),
						FileReference:    getDataString(dataArray, getInt(parsedArray, i-6)),
						PartyName:        getDataString(dataArray, getInt(parsedArray, i-8)),
						Status:           getDataString(dataArray, getInt(parsedArray, i-9)),
						TravelDate:       getDataString(dataArray, getInt(parsedArray, i-10)),
					}

					if companyCodeIdx := getInt(parsedArray, i-1); companyCodeIdx > 0 && companyCodeIdx < len(dataArray) {
						result.CompanyCode = getDataString(dataArray, companyCodeIdx)
					}

					response.Results = append(response.Results, result)
					i -= 10
				}
			}
		}
	} else if strings.HasPrefix(mappedFirstStringValue, "com.lynxtraveltech.client.shared.model.FileSearchResponse") {
		for i := len(parsedArray) - 6; i >= 0; i-- {
			if idx, ok := parsedArray[i].(int); ok {
				if idx <= 0 || idx >= len(dataArray) {
					continue
				}

				currentValue := dataArray[idx-1]
				if currentStringValue, ok := currentValue.(string); ok && strings.HasPrefix(currentStringValue, GWTTypeFileSearchResults) {
					result := FileSearchResult{
						CompanyCode:      getDataString(dataArray, getInt(parsedArray, i-1)),
						ClientIdentifier: getString(parsedArray, i-2),
						ClientReference:  getDataString(dataArray, getInt(parsedArray, i-3)),
						Currency:         getDataString(dataArray, getInt(parsedArray, i-4)),
						FileIdentifier:   getString(parsedArray, i-5),
						FileReference:    getDataString(dataArray, getInt(parsedArray, i-6)),
						PartyName:        getDataString(dataArray, getInt(parsedArray, i-8)),
						Status:           getDataString(dataArray, getInt(parsedArray, i-9)),
						TravelDate:       getDataString(dataArray, getInt(parsedArray, i-10)),
					}
					response.Results = append(response.Results, result)
					i -= 10
				}
			}
		}
	}

	return &response, nil
}

func ParseRetrieveItineraryResponse(responseBody string) (*ItineraryResponse, error) {
	if !strings.HasPrefix(responseBody, "//OK") {
		return nil, fmt.Errorf("response body missing //OK")
	}

	body := strings.TrimPrefix(responseBody, "//OK")
	parsedArray, err := ParseGWTArray(body)
	if err != nil {
		return nil, fmt.Errorf("failed to parse main array: %w", err)
	}

	if len(parsedArray) < 4 {
		return nil, fmt.Errorf("response too short: %d items", len(parsedArray))
	}

	dataArray, ok := parsedArray[len(parsedArray)-3].([]interface{})
	if !ok {
		return nil, fmt.Errorf("expected data array")
	}

	response := ItineraryResponse{
		Type:             getDataString(dataArray, getInt(parsedArray, 1)),
		PartyName:        getDataString(dataArray, getInt(parsedArray, 2)),
		FileReference:    getDataString(dataArray, getInt(parsedArray, 4)),
		FileIdentifier:   getString(parsedArray, 5),
		AgentReference:   getDataString(dataArray, getInt(parsedArray, 7)),
		ClientIdentifier: getString(parsedArray, 8),
		Itineraries:      make([]ItineraryItem, 0),
	}

	var items []struct {
		it     ItineraryItem
		parts  []descEntry
		exIdx  map[int]bool
	}

	// GWT serialises in reverse order, so we scan backwards through parsedArray.
	// Each TransactionSummary marker is the anchor for one itinerary item.
	// Fields appear at fixed offsets *after* the anchor in the backward-encoded
	// stream (i.e. at higher parsedArray indices when scanning forward, but we
	// encounter them *before* the anchor when scanning backwards).
	//
	// Scanning backwards: anchor at position i, then fields at i+1, i+3, i+6, i+10
	// for VoucherIdentifier, Date, Supplier, Status respectively.
	// ConfirmationNumber and Location are at i-9 and i-14 (lower indices = fields
	// that were emitted after this item's anchor in the forward stream, belonging
	// to the *next* item's header — so we read them from the *previous* anchor's
	// backward window instead, i.e. from *after* the current anchor going forward).

	// First pass: find all TransactionSummary anchor positions (scanning backwards).
	type anchorInfo struct {
		pos  int // index in parsedArray
		item ItineraryItem
	}
	var anchors []anchorInfo

	for i := len(parsedArray) - 4; i >= 11; i-- {
		idx, ok := parsedArray[i].(int)
		if !ok || idx <= 0 || idx >= len(dataArray) {
			continue
		}
		sv, ok := dataArray[idx-1].(string)
		if !ok {
			continue
		}
		if strings.HasPrefix(sv, GWTTypeTransactionSummaryClient) || strings.HasPrefix(sv, GWTTypeTransactionSummaryCommon) {
			anchors = append(anchors, anchorInfo{pos: i})
		}
	}

	// Second pass: for each anchor, collect fields from the window of parsedArray
	// entries *before* this anchor (between the previous anchor and this one).
	// Because GWT is reversed, the fields preceding anchor[n] in the stream belong
	// to anchor[n]'s item. The window runs from prevAnchor.pos+1 (or index 10 for
	// the first item) up to anchor.pos-1.
	//
	// Within that window, the first valid data index is the VoucherIdentifier,
	// followed by a null, then Date, then TransactionIdentifier (string), then
	// optionally a type descriptor pair, then Supplier, then further down Status.
	// We identify each field by scanning the window and matching by position.
	for a, anchor := range anchors {
		item := ItineraryItem{}
		excludeIdx := make(map[int]bool)
		var descParts []descEntry

		// Window: entries before this anchor belonging to this item.
		// Anchors are found scanning backwards (highest pa index first), so
		// anchors[a+1] has a smaller pa index than anchors[a].
		// The window for this item runs from anchors[a+1].pos+1 up to anchor.pos-1.
		windowStart := 10 // pa[10] is the first item-data slot
		if a+1 < len(anchors) {
			windowStart = anchors[a+1].pos + 1
		}
		windowEnd := anchor.pos - 1

		// Scan the window before the anchor to extract structured fields.
		// The GWT layout within the window (reading forward = reverse of GWT encoding):
		//
		//   slot 0: VoucherIdentifier (null/0 when absent)
		//   slot 1: null
		//   slot 2: Date
		//   slot 3+4: java.lang.Long type descriptor + value (skipped, rel+=2)
		//   slot 5: Supplier
		//   slot 6: empty string ""
		//   slot 7: raw single-letter status flag ("A", "S"…) — skip
		//   slot 8: Status (human-readable)
		//
		// When slot 0 is null (no voucher), all slots shift by +1 (offset=1).
		// Type descriptor pairs are skipped and their two slots counted in rel.
		rel := 0
		offset := 0 // +1 when slot 0 is null (voucher absent)
		for i := windowStart; i <= windowEnd; i++ {
			switch v := parsedArray[i].(type) {
			case string:
				// TransactionIdentifier is encoded as a raw string in this window.
				if item.TransactionIdentifier == "" && len(v) > 3 && strings.HasPrefix(v, "B") && v[1] >= 'a' && v[1] <= 'z' {
					item.TransactionIdentifier = v
				}
				continue
			case int:
				if v <= 0 || v >= len(dataArray) {
					if rel == 0 {
						offset = 1 // leading null = no voucher, shift all offsets
					}
					rel++
					continue
				}
				raw, ok := dataArray[v-1].(string)
				if !ok {
					rel++
					continue
				}
				// Skip type descriptor pairs (type token + value token),
				// counting both slots so rel stays in sync.
				if strings.HasPrefix(raw, GWTTypeBigDecimal) ||
					strings.HasPrefix(raw, GWTTypeSQLDate) ||
					strings.HasPrefix(raw, GWTTypeDouble) ||
					strings.HasPrefix(raw, GWTTypeLong) ||
					strings.HasPrefix(raw, GWTTypeString) {
					i++   // skip value token
					rel++ // count type token
					rel++ // count value token
					continue
				}
				sv := unescapeGWT(raw)
				switch rel - offset {
				case 0:
					item.VoucherIdentifier = sv
					excludeIdx[v] = true
				case 2:
					item.Date = sv
					excludeIdx[v] = true
				case 5:
					item.Supplier = sv
					excludeIdx[v] = true
				case 8:
					item.Status = sv
					excludeIdx[v] = true
				default:
					if isDescriptive(sv) {
						descParts = append(descParts, descEntry{index: v, value: sv})
					}
				}
				rel++
			default:
				// float64 or other — skip
			}
		}

		// ConfirmationNumber and Location are at fixed offsets before the anchor.
		if cfrnNumIdx := getInt(parsedArray, anchor.pos-9); cfrnNumIdx > 0 && cfrnNumIdx < len(dataArray) {
			item.ConfirmationNumber = getDataString(dataArray, cfrnNumIdx)
			excludeIdx[cfrnNumIdx] = true
		}
		if locIdx := getInt(parsedArray, anchor.pos-14); locIdx > 0 && locIdx < len(dataArray) {
			item.Location = getDataString(dataArray, locIdx)
			excludeIdx[locIdx] = true
		}

		anchors[a].item = item
		items = append(items, struct {
			it    ItineraryItem
			parts []descEntry
			exIdx map[int]bool
		}{item, descParts, excludeIdx})
	}

	valueFreq := make(map[string]int)
	for _, it := range items {
		seen := make(map[string]bool)
		for _, p := range it.parts {
			trimmed := strings.TrimSpace(p.value)
			if trimmed == "" || seen[trimmed] {
				continue
			}
			seen[trimmed] = true
			valueFreq[trimmed]++
		}
	}

	for _, it := range items {
		uniq := make([]string, 0, len(it.parts))
		seen := make(map[string]bool)
		for _, p := range it.parts {
			trimmed := strings.TrimSpace(p.value)
			if trimmed == "" || seen[trimmed] || it.exIdx[p.index] || valueFreq[trimmed] >= 5 {
				continue
			}
			seen[trimmed] = true
			uniq = append(uniq, trimmed)
		}
		it.it.Description = strings.Join(uniq, " | ")
		response.ItineraryCount++
		response.Itineraries = append(response.Itineraries, it.it)
	}

	return &response, nil
}

func ParseFileDocumentsResponse(responseBody string) (*FileDocumentsResponse, error) {
	if !strings.HasPrefix(responseBody, "//OK") {
		return nil, fmt.Errorf("response body missing //OK")
	}

	body := strings.TrimPrefix(responseBody, "//OK")
	parsedArray, err := ParseGWTArray(body)
	if err != nil {
		return nil, fmt.Errorf("failed to parse main array: %w", err)
	}

	if len(parsedArray) < 4 {
		return nil, fmt.Errorf("response too short: %d items", len(parsedArray))
	}

	dataArray, ok := parsedArray[len(parsedArray)-3].([]interface{})
	if !ok {
		return nil, fmt.Errorf("expected data array")
	}

	oneBasedIndex, ok := parsedArray[len(parsedArray)-4].(int)
	if !ok {
		return nil, fmt.Errorf("expected one-based index")
	}

	mappedFirstStringValue, ok := dataArray[oneBasedIndex-1].(string)
	if !ok {
		return nil, fmt.Errorf("expected string value")
	}

	if !strings.HasPrefix(mappedFirstStringValue, GWTTypeArray) {
		return nil, fmt.Errorf("first item should be an array")
	}

	arraySize, ok := parsedArray[len(parsedArray)-5].(int)
	if !ok {
		return nil, fmt.Errorf("expected array size")
	}

	response := FileDocumentsResponse{
		Count:   arraySize,
		Results: make([]FileDocument, 0, arraySize),
	}

	for i := len(parsedArray) - 6; i >= 0; i-- {
		if idx, ok := parsedArray[i].(int); ok {
			if idx <= 0 || idx >= len(dataArray) {
				continue
			}

			currentValue := dataArray[idx-1]
			if currentStringValue, ok := currentValue.(string); ok && strings.HasPrefix(currentStringValue, GWTTypeDocumentDetails) {
				doc := FileDocument{
					TransactionIdentifier: getString(parsedArray, i-2),
					
					DocumentType:          getDataString(dataArray, getInt(parsedArray, i-12)),
					FileIdentifier:        getString(parsedArray, i-14),
					DocumentName:          getDataString(dataArray, getInt(parsedArray, i-15)),
					DocumentIdentifier:    getString(parsedArray, i-10),
				}

				if attachmentIdx := getInt(parsedArray, i-16); attachmentIdx > 0 {
					doc.AttachmentURL = getDataString(dataArray, attachmentIdx)
				}

				response.Results = append(response.Results, doc)
				i -= 17
			}
		}
	}

	return &response, nil
}

func ParseSaveResponse(responseBody string) error {
	if !strings.HasPrefix(responseBody, "//OK") {
		return fmt.Errorf("save failed: response missing //OK")
	}
	return nil
}

func ParseErrorResponse(responseBody string) (string, error) {
	body := strings.TrimPrefix(responseBody, "//EX")
	parsedArray, err := ParseGWTArray(body)
	if err != nil {
		return "", fmt.Errorf("failed to parse error array: %w", err)
	}

	if len(parsedArray) < 3 {
		return "", fmt.Errorf("error response too short")
	}

	errorArray, ok := parsedArray[2].([]interface{})
	if !ok {
		return "", fmt.Errorf("third item is not an array")
	}

	var parts []string
	for i := 1; i < len(errorArray); i++ {
		if msgPart, ok := errorArray[i].(string); ok {
			parts = append(parts, msgPart)
		}
	}

	if len(parts) == 0 {
		return "", fmt.Errorf("no error message found")
	}

	return unescapeGWT(strings.Join(parts, ", ")), nil
}

func getString(arr []interface{}, idx int) string {
	if idx >= 0 && idx < len(arr) {
		if s, ok := arr[idx].(string); ok {
			return s
		}
	}
	return ""
}

func getInt(arr []interface{}, idx int) int {
	if idx >= 0 && idx < len(arr) {
		if n, ok := arr[idx].(int); ok {
			return n
		}
	}
	return 0
}

type descEntry struct {
	index int
	value string
}

func getDataString(data []interface{}, idx int) string {
	if idx > 0 && idx <= len(data) {
		if s, ok := data[idx-1].(string); ok {
			return unescapeGWT(s)
		}
	}
	return ""
}

func isDescriptive(s string) bool {
	if len(s) < 3 {
		return false
	}
	trimmed := strings.TrimSpace(s)
	if trimmed == "" || trimmed == "-" {
		return false
	}
	if strings.HasPrefix(trimmed, "java.") || strings.HasPrefix(trimmed, "com.lynxtraveltech") {
		return false
	}
	if strings.HasPrefix(trimmed, "AUD") || strings.HasPrefix(trimmed, "$") {
		return false
	}
	if strings.HasSuffix(trimmed, "%") && len(trimmed) < 10 {
		return false
	}
	if _, err := strconv.ParseFloat(trimmed, 64); err == nil {
		return false
	}
	if _, err := strconv.Atoi(trimmed); err == nil {
		return false
	}
	if len(trimmed) == 1 {
		return false
	}
	if len(trimmed) <= 4 && strings.ContainsAny(trimmed, "0123456789") {
		return false
	}
	if strings.Contains(trimmed, "N/A") {
		return false
	}
	if trimmed == "A" || trimmed == "S" || trimmed == "C" || trimmed == "B" || trimmed == "D" || trimmed == "SM" {
		return false
	}
	if isTimestamp(trimmed) {
		return false
	}
	if isLocation(trimmed) {
		return false
	}
	return true
}

func isTimestamp(s string) bool {
	parts := strings.Fields(s)
	if len(parts) < 2 {
		return false
	}
	return isDateLike(parts[0]) && isMonthName(parts[1])
}

func isDateLike(s string) bool {
	if len(s) < 2 {
		return false
	}
	for _, c := range s {
		if c >= '0' && c <= '9' {
			return true
		}
	}
	return false
}

var monthNames = map[string]bool{
	"Jan": true, "Feb": true, "Mar": true, "Apr": true,
	"May": true, "Jun": true, "Jul": true, "Aug": true,
	"Sep": true, "Oct": true, "Nov": true, "Dec": true,
}

func isMonthName(s string) bool {
	return monthNames[s]
}

func isLocation(s string) bool {
	parts := strings.Split(s, ",")
	if len(parts) != 2 {
		return false
	}
	state := strings.TrimSpace(parts[1])
	return len(state) <= 3 && strings.ToUpper(state) == state && len(state) > 0 && !strings.Contains(state, " ")
}


