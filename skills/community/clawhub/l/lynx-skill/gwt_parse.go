package main

import (
	"fmt"
	"strconv"
	"strings"
)

func parseGWTArray(arrayStr string) ([]interface{}, error) {
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
		return parseGWTArray(element)
	}
	return element, nil
}

func unescapeGWTString(s string) string {
	s = strings.Trim(s, "\"")
	s = strings.ReplaceAll(s, "\\\"", "\"")
	var result strings.Builder
	for i := 0; i < len(s); i++ {
		if i+3 < len(s) && s[i] == '\\' && s[i+1] == 'x' {
			hexStr := s[i+2 : i+4]
			if val, err := strconv.ParseUint(hexStr, 16, 8); err == nil {
				result.WriteByte(byte(val))
				i += 3
			} else {
				result.WriteByte(s[i])
			}
		} else {
			result.WriteByte(s[i])
		}
	}
	return result.String()
}

type FileSearchResult struct {
	CompanyCode      string `json:"companyCode"`
	ClientIdentifier string `json:"clientIdentifier"`
	ClientReference  string `json:"clientReference"`
	Currency         string `json:"currency"`
	FileIdentifier   string `json:"fileIdentifier"`
	FileReference    string `json:"fileReference"`
	PartyName        string `json:"partyName"`
	Status           string `json:"status"`
	TravelDate       string `json:"traveDate"`
}

type FileSearchResponse struct {
	Count   int                `json:"count"`
	Results []FileSearchResult `json:"results"`
}

func parseFileSearchResponseBody(responseBody string) (*FileSearchResponse, error) {
	if !strings.HasPrefix(responseBody, "//OK") {
		return nil, fmt.Errorf("response body missing //OK")
	}

	body := strings.TrimPrefix(responseBody, "//OK")
	parsedArray, err := parseGWTArray(body)
	if err != nil {
		return nil, fmt.Errorf("failed to parse main array: %w", err)
	}

	if len(parsedArray) < 4 {
		return nil, fmt.Errorf("response body should contain at least 4 items, got %d", len(parsedArray))
	}

	if parsedArray[len(parsedArray)-1] != 7 {
		return nil, fmt.Errorf("response body should contain protocol version 7, got %d", parsedArray[len(parsedArray)-1])
	}

	dataArray, ok := parsedArray[len(parsedArray)-3].([]interface{})
	if !ok {
		return nil, fmt.Errorf("response body should contain a data array, got %T", parsedArray[len(parsedArray)-3])
	}

	oneBasedIndex, ok := parsedArray[len(parsedArray)-4].(int)
	if !ok {
		return nil, fmt.Errorf("expected one-based index, got %T", parsedArray[len(parsedArray)-4])
	}

	mappedFirstStringValue, ok := dataArray[oneBasedIndex-1].(string)
	if !ok {
		return nil, fmt.Errorf("expected string value, got %T", dataArray[oneBasedIndex-1])
	}

	if !strings.HasPrefix(mappedFirstStringValue, gwtTypeArray) {
		return nil, fmt.Errorf("first item should be an array, got %T", mappedFirstStringValue)
	}

	arraySize, ok := parsedArray[len(parsedArray)-5].(int)
	if !ok {
		return nil, fmt.Errorf("first array item should have a size, got %T", parsedArray[len(parsedArray)-5])
	}

	fileSearchResponse := FileSearchResponse{
		Count:   arraySize,
		Results: make([]FileSearchResult, arraySize),
	}

	for i, resultIndex := len(parsedArray)-6, 0; i >= 0; i-- {
		if oneBasedIndex, ok := parsedArray[i].(int); ok {
			if oneBasedIndex <= 0 || oneBasedIndex >= len(dataArray) {
				continue
			}

			currentValue := dataArray[oneBasedIndex-1]

			if currentStringValue, ok := currentValue.(string); ok && strings.HasPrefix(currentStringValue, gwtTypeFileSearchResults) {
				fileSearchResult := FileSearchResult{
					ClientIdentifier: parsedArray[i-2].(string),
					ClientReference:  dataArray[parsedArray[i-3].(int)-1].(string),
					Currency:         dataArray[parsedArray[i-4].(int)-1].(string),
					FileIdentifier:   parsedArray[i-5].(string),
					FileReference:    dataArray[parsedArray[i-6].(int)-1].(string),
					PartyName:        unescapeGWTString(dataArray[parsedArray[i-8].(int)-1].(string)),
					Status:           dataArray[parsedArray[i-9].(int)-1].(string),
					TravelDate:       dataArray[parsedArray[i-10].(int)-1].(string),
				}

				if companyCodeIdx, ok := parsedArray[i-1].(int); ok && companyCodeIdx > 0 && companyCodeIdx <= len(dataArray) {
					fileSearchResult.CompanyCode = dataArray[companyCodeIdx-1].(string)
				}

				fileSearchResponse.Results[resultIndex] = fileSearchResult
				i = i - 10
				resultIndex++
			}
		}
	}

	return &fileSearchResponse, nil
}

type FileDocument struct {
	FileIdentifier        string `json:"fileIdentifier"`
	TransactionIdentifier string `json:"transactionIdentifier"`
	DocumentIdentifier    string `json:"documentIdentifier"`
	DocumentName          string `json:"documentName"`
	DocumentType          string `json:"documentType"`
	Content               string `json:"content"`
	AttachmentUrl         string `json:"attachmentUrl"`
}

type FileDocumentsResponse struct {
	Count   int            `json:"count"`
	Results []FileDocument `json:"results"`
}

func parseFileDocumentsListResponseBody(responseBody string) (*FileDocumentsResponse, error) {
	if !strings.HasPrefix(responseBody, "//OK") {
		return nil, fmt.Errorf("response body missing //OK")
	}

	body := strings.TrimPrefix(responseBody, "//OK")
	parsedArray, err := parseGWTArray(body)
	if err != nil {
		return nil, fmt.Errorf("failed to parse main array: %w", err)
	}

	if len(parsedArray) < 4 {
		return nil, fmt.Errorf("response body should contain at least 4 items, got %d", len(parsedArray))
	}

	if parsedArray[len(parsedArray)-1] != 7 {
		return nil, fmt.Errorf("response body should contain protocol version 7, got %d", parsedArray[len(parsedArray)-1])
	}

	dataArray, ok := parsedArray[len(parsedArray)-3].([]interface{})
	if !ok {
		return nil, fmt.Errorf("response body should contain a data array, got %T", parsedArray[len(parsedArray)-3])
	}

	oneBasedIndex, ok := parsedArray[len(parsedArray)-4].(int)
	if !ok {
		return nil, fmt.Errorf("expected one-based index, got %T", parsedArray[len(parsedArray)-4])
	}

	mappedFirstStringValue, ok := dataArray[oneBasedIndex-1].(string)
	if !ok {
		return nil, fmt.Errorf("expected string value, got %T", dataArray[oneBasedIndex-1])
	}

	if !strings.HasPrefix(mappedFirstStringValue, gwtTypeArray) {
		return nil, fmt.Errorf("first item should be an array, got %T", mappedFirstStringValue)
	}

	arraySize, ok := parsedArray[len(parsedArray)-5].(int)
	if !ok {
		return nil, fmt.Errorf("first array item should have a size, got %T", parsedArray[len(parsedArray)-5])
	}

	fileDocumentsResponse := FileDocumentsResponse{
		Count:   arraySize,
		Results: make([]FileDocument, arraySize),
	}

	for i, resultIndex := len(parsedArray)-6, 0; i >= 0; i-- {
		if oneBasedIndex, ok := parsedArray[i].(int); ok {
			if oneBasedIndex <= 0 || oneBasedIndex >= len(dataArray) {
				continue
			}

			currentValue := dataArray[oneBasedIndex-1]

			if currentStringValue, ok := currentValue.(string); ok && strings.HasPrefix(currentStringValue, gwtTypeDocumentDetails) {
				fileDocument := FileDocument{
					TransactionIdentifier: parsedArray[i-2].(string),
					Content:               unescapeGWTString(dataArray[parsedArray[i-11].(int)-1].(string)),
					DocumentType:          dataArray[parsedArray[i-13].(int)-1].(string),
					FileIdentifier:        parsedArray[i-14].(string),
					DocumentName:          dataArray[parsedArray[i-15].(int)-1].(string),
					DocumentIdentifier:    dataArray[parsedArray[i-17].(int)-1].(string),
				}

				if attachmentIdx, ok := parsedArray[i-16].(int); ok && attachmentIdx > 0 {
					fileDocument.AttachmentUrl = dataArray[attachmentIdx-1].(string)
				}

				fileDocumentsResponse.Results[resultIndex] = fileDocument
				i -= 17
				resultIndex++
			}
		}
	}

	return &fileDocumentsResponse, nil
}

type ItineraryTransactionSummary struct {
	VoucherIdentifier     string `json:"voucherIdentifier"`
	Date                  string `json:"date"`
	TransactionIdentifier string `json:"transactionIdentifier"`
	Supplier              string `json:"supplier"`
	Status                string `json:"status"`
	ConfirmationNumber    string `json:"confirmationNumber"`
	Location              string `json:"location"`
}

type RetrieveItineraryResponse struct {
	Type             string                        `json:"type"`
	PartyName        string                        `json:"partyName"`
	FileReference    string                        `json:"fileReference"`
	FileIdentifier   string                        `json:"fileIdentifier"`
	ClientIdentifier string                        `json:"clientIdentifier"`
	AgentReference   string                        `json:"agentReference"`
	ItineraryCount   int                           `json:"itineraryCount"`
	Itineraries      []ItineraryTransactionSummary `json:"itineraries"`
}

func parseRetrieveItineraryResponseBody(responseBody string) (*RetrieveItineraryResponse, error) {
	if !strings.HasPrefix(responseBody, "//OK") {
		return nil, fmt.Errorf("response body missing //OK")
	}

	body := strings.TrimPrefix(responseBody, "//OK")
	parsedArray, err := parseGWTArray(body)
	if err != nil {
		return nil, fmt.Errorf("failed to parse main array: %w", err)
	}

	if len(parsedArray) < 4 {
		return nil, fmt.Errorf("response body should contain at least 4 items, got %d", len(parsedArray))
	}

	if parsedArray[len(parsedArray)-1] != 7 {
		return nil, fmt.Errorf("response body should contain protocol version 7, got %d", parsedArray[len(parsedArray)-1])
	}

	dataArray, ok := parsedArray[len(parsedArray)-3].([]interface{})
	if !ok {
		return nil, fmt.Errorf("response body should contain a data array, got %T", parsedArray[len(parsedArray)-3])
	}

	response := RetrieveItineraryResponse{
		Type:             dataArray[parsedArray[1].(int)-1].(string),
		PartyName:        unescapeGWTString(dataArray[parsedArray[2].(int)-1].(string)),
		FileReference:    dataArray[parsedArray[4].(int)-1].(string),
		FileIdentifier:   parsedArray[5].(string),
		AgentReference:   dataArray[parsedArray[7].(int)-1].(string),
		ClientIdentifier: parsedArray[8].(string),
		ItineraryCount:   0,
		Itineraries:      make([]ItineraryTransactionSummary, 0),
	}

	currentItinerary := ItineraryTransactionSummary{}

	for i, rel := 11, 0; i < len(parsedArray); i, rel = i+1, rel+1 {
		if stringValue, ok := parsedArray[i].(string); ok {
			switch rel {
			case 3:
				currentItinerary.TransactionIdentifier = stringValue
			}

			if currentItinerary.TransactionIdentifier == "" &&
				len(stringValue) > 3 &&
				strings.HasPrefix(stringValue, "B") &&
				len(stringValue) > 2 &&
				stringValue[1:2] >= "a" &&
				stringValue[1:2] <= "z" {
				currentItinerary.TransactionIdentifier = stringValue
			}
		}

		if oneBasedIndex, ok := parsedArray[i].(int); ok {
			if oneBasedIndex <= 0 || oneBasedIndex >= len(dataArray) {
				continue
			}

			currentValue := dataArray[oneBasedIndex-1]

			if currentStringValue, ok := currentValue.(string); ok &&
				(strings.HasPrefix(currentStringValue, gwtTypeBigDecimal) ||
					strings.HasPrefix(currentStringValue, gwtTypeSQLDate) ||
					strings.HasPrefix(currentStringValue, gwtTypeDouble) ||
					strings.HasPrefix(currentStringValue, gwtTypeLong) ||
					strings.HasPrefix(currentStringValue, gwtTypeString)) {
				i++
				continue
			}

			switch rel {
			case 0:
				currentItinerary.VoucherIdentifier = currentValue.(string)
			case 2:
				currentItinerary.Date = currentValue.(string)
			case 5:
				currentItinerary.Supplier = currentValue.(string)
			case 9:
				currentItinerary.Status = currentValue.(string)
			}

			if currentStringValue, ok := currentValue.(string); ok && strings.HasPrefix(currentStringValue, gwtTypeTransactionSummary) {
				oneBasedIndexCfrnNum, ok := parsedArray[i-9].(int)
				if ok && oneBasedIndexCfrnNum > 0 && oneBasedIndexCfrnNum < len(dataArray) {
					currentItinerary.ConfirmationNumber = dataArray[oneBasedIndexCfrnNum-1].(string)
				}

				oneBasedIndexLoc, ok := parsedArray[i-14].(int)
				if ok && oneBasedIndexLoc > 0 && oneBasedIndexLoc < len(dataArray) {
					currentItinerary.Location = dataArray[oneBasedIndexLoc-1].(string)
				}

				response.ItineraryCount += 1
				response.Itineraries = append(response.Itineraries, currentItinerary)

				currentItinerary = ItineraryTransactionSummary{}
				rel = -1
			}
		}
	}

	for i, j := 0, len(response.Itineraries)-1; i < j; i, j = i+1, j-1 {
		response.Itineraries[i], response.Itineraries[j] = response.Itineraries[j], response.Itineraries[i]
	}

	return &response, nil
}
