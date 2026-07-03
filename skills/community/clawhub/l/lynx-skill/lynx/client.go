package lynx

import (
	"fmt"
	"io"
	"net/http"
	"strconv"
	"strings"
)

const cookiePath = "/lynx"

func doRequest(client *http.Client, remoteHost, urlPath, contentType, body string) (string, int, error) {
	req, err := http.NewRequest("POST", fmt.Sprintf("https://%s%s", remoteHost, urlPath), strings.NewReader(body))
	if err != nil {
		return "", 0, fmt.Errorf("failed to create request: %w", err)
	}

	req.Header.Set("Content-Type", contentType)

	resp, err := client.Do(req)
	if err != nil {
		return "", 0, fmt.Errorf("failed to execute request: %w", err)
	}
	defer resp.Body.Close()

	respBody, err := io.ReadAll(resp.Body)
	if err != nil {
		return "", resp.StatusCode, fmt.Errorf("failed to read response body: %w", err)
	}

	bodyStr := string(respBody)

	if resp.StatusCode == http.StatusOK && strings.HasPrefix(bodyStr, "//EX") {
		errMsg, parseErr := parseGWTError(bodyStr)
		if parseErr == nil {
			return "", resp.StatusCode, fmt.Errorf("GWT error: %s", errMsg)
		}
		return "", resp.StatusCode, fmt.Errorf("GWT error (unparseable): %s", bodyStr)
	}

	return bodyStr, resp.StatusCode, nil
}

func DoGWTRequest(client *http.Client, remoteHost, urlPath, body string) (string, error) {
	respBody, statusCode, err := doRequest(client, remoteHost, urlPath, "text/x-gwt-rpc; charset=utf-8", body)
	if err != nil {
		return "", err
	}
	if statusCode != http.StatusOK {
		return "", fmt.Errorf("request failed with status %d: %s", statusCode, respBody)
	}
	return respBody, nil
}

type MultipartForm struct {
	Fields map[string]string
	File   struct {
		FieldName string
		FileName  string
		Data      []byte
	}
}

func DoMultipartRequest(client *http.Client, remoteHost, urlPath string, form *MultipartForm) (string, error) {
	boundary := "----lynxskillboundary123"

	var requestBody strings.Builder

	for key, value := range form.Fields {
		requestBody.WriteString(fmt.Sprintf("--%s\r\n", boundary))
		requestBody.WriteString(fmt.Sprintf("Content-Disposition: form-data; name=\"%s\"\r\n\r\n", key))
		requestBody.WriteString(value)
		requestBody.WriteString("\r\n")
	}

	if form.File.Data != nil {
		requestBody.WriteString(fmt.Sprintf("--%s\r\n", boundary))
		requestBody.WriteString(fmt.Sprintf("Content-Disposition: form-data; name=\"%s\"; filename=\"%s\"\r\n", form.File.FieldName, form.File.FileName))
		requestBody.WriteString("Content-Type: application/octet-stream\r\n\r\n")
		requestBody.Write(form.File.Data)
		requestBody.WriteString("\r\n")
	}

	requestBody.WriteString(fmt.Sprintf("--%s--\r\n", boundary))

	contentType := fmt.Sprintf("multipart/form-data; boundary=%s", boundary)

	respBody, statusCode, err := doRequest(client, remoteHost, urlPath, contentType, requestBody.String())
	if err != nil {
		return "", err
	}
	if statusCode != http.StatusOK {
		return "", fmt.Errorf("request failed with status %d: %s", statusCode, respBody)
	}

	return respBody, nil
}

func parseGWTError(responseBody string) (string, error) {
	body := strings.TrimPrefix(responseBody, "//EX")
	parsedArray, err := parseGWTArray(body)
	if err != nil {
		return "", err
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

	return strings.Join(parts, ", "), nil
}

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
